import logging
from functools import wraps

import confight
from flask import Flask
from flask import jsonify
from flask import request
from gunicorn.six import iteritems
from gunicorn.app.base import BaseApplication

from docker_volume_nest.defaults import DEFAULTS
from .driver import HookedDriver

app = Flask(__name__)
DEFAULT_BASE = '/mnt'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class MountMgr(object):
    """ MountMgr is a helper class used during mounting/unmounting."""

    def __init__(self, counter, mntpoint):
        self.counter = counter
        self.mntpoint = mntpoint


class VolumeManager(object):
    """
    VolumeManager is the class providing pluggable drivers
    the drivers implementing the methods:
       1. create
       2. list
       3. path
       4. remove
       5. mount
       6. umount
       7. scope
       8. cleanup
    """

    def __init__(self, config):
        self.driver = HookedDriver(config)
        self.mount_mgr = {}

    def cleanup(self):
        """ Cleanup done during shutdown of server."""
        for volume in self.mount_mgr:
            self.mount_mgr[volume].counter = 0
            self.mount_mgr[volume].mntpoint = None
        self.driver.cleanup()


def normalize(f):
    """ To jsonify the response with correct HTTP status code.
    Status codes:
        200: OK
        400: Error
    Err in JSON is non empty if there is an error.
    """
    @wraps(f)
    def inner_function(*args, **kwargs):
        data = f(*args, **kwargs)
        if 'Err' in data and data['Err'] != "":
            code = 400
        else:
            code = 200
        resp = jsonify(data)
        resp.status_code = code
        return resp
    return inner_function


@app.route('/Plugin.Activate', methods=['POST'])
@normalize
def implements():
    """ Routes Docker Volume '/Plugin.Activate'."""
    return {"Implements": ["VolumeDriver"]}


@app.route('/VolumeDriver.Create', methods=['POST'])
@normalize
def create_volume():
    """ Routes Docker Volume '/VolumeDriver.Create'."""
    volm = app.config['volmer']
    rdata = request.get_json(force=True)
    vol_name = rdata['Name'].strip('/')
    options = rdata['Opts']

    try:
        volm.driver.create(vol_name, options)
    except Exception as e:
        return {
            "Err": "Failed to create the volume {0} : {1}".format(
                vol_name, str(e)
            )
        }
    return {"Err": ""}


@app.route('/')
def index():
    return 'Docker volume driver listening'


@app.route('/VolumeDriver.Remove', methods=['POST'])
@normalize
def remove_volume():
    """ Routes Docker Volume '/VolumeDriver.Remove'."""
    volm = app.config['volmer']
    rdata = request.get_json(force=True)
    vol_name = rdata['Name'].strip('/')
    try:
        volm.driver.remove(vol_name)
    except Exception as e:
        return {
            "Err": "Failed to remove the volume {0}: {1}".format(
                vol_name, str(e)
            )
        }
    return {"Err": ""}


@app.route('/VolumeDriver.Mount', methods=['POST'])
@normalize
def mount_volume():
    """ Routes Docker Volume '/VolumeDriver.Mount'.
    Handles multiple invocations of mount for same volume.
    """
    volm = app.config['volmer']
    rdata = request.get_json(force=True)
    vol_name = rdata['Name'].strip('/')
    # vol_id = rdata['ID']

    if vol_name in volm.mount_mgr:
        mntpoint = volm.mount_mgr[vol_name].mntpoint
        volm.mount_mgr[vol_name].counter += 1
        log.info(
            "Volume {0} is mounted {1} times".format(
                vol_name, volm.mount_mgr[vol_name].counter
            )
        )
        return {"Mountpoint": mntpoint, "Err": ""}

    try:
        mntpoint = volm.driver.mount(vol_name)
        volm.mount_mgr[vol_name] = MountMgr(1, mntpoint)
    except Exception as e:
        return {
            "Mountpoint": "",
            "Err": "Failed to mount the volume {0}: {1}".format(
                vol_name, str(e)
            )
        }
    return {"Mountpoint": mntpoint, "Err": ""}


@app.route('/VolumeDriver.Path', methods=['POST'])
@normalize
def path_volume():
    """ Routes Docker Volume '/VolumeDriver.Path'.
    Returns Err if volume is not mounted.
    """
    volm = app.config['volmer']
    rdata = request.get_json(force=True)
    vol_name = rdata['Name'].strip('/')
    try:
        mntpoint = volm.driver.path(vol_name)
    except Exception as e:
        return {
            "Mountpoint": "",
            "Err": "Failed to obtain path to the volume {0}: {1}".format(
                vol_name, str(e)
            )
        }
    if not mntpoint:
        return {
            "Mountpoint": "",
            "Err": "Volume {0} is not mounted".format(vol_name)
        }
    return {"Mountpoint": mntpoint, "Err": ""}


@app.route('/VolumeDriver.Unmount', methods=['POST'])
@normalize
def unmount_volume():
    """ Routes Docker Volume '/VolumeDriver.Unmount'.
        Handles multiple Unmount requests for volume mounted multiple
        times by only unmounting the last time.
    """
    volm = app.config['volmer']
    rdata = request.get_json(force=True)
    vol_name = rdata['Name'].strip('/')
    # vol_id = rdata['ID']

    if vol_name in volm.mount_mgr:
        # mntpoint = volm.mount_mgr[vol_name].mntpoint
        volm.mount_mgr[vol_name].counter -= 1
        if volm.mount_mgr[vol_name].counter > 0:
            log.info(
                "Still mounted {0} times to unmount".format(
                    volm.mount_mgr[vol_name].counter
                )
            )
            return {"Err": ""}

    try:
        res = volm.driver.umount(vol_name)
        if not res:
            return {
                "Err": "Volume {0} may already be unmounted.".format(vol_name)
            }
        volm.mount_mgr.pop(vol_name)
    except Exception as e:
        return {
            "Err": "Failed to umount the volume {0}: {1}".format(
                vol_name, str(e))
        }

    return {"Err": ""}


@app.route('/VolumeDriver.Get', methods=['POST'])
@normalize
def get_volume():
    """ Routes Docker Volume '/VolumeDriver.Get'."""
    volm = app.config['volmer']
    rdata = request.get_json(force=True)
    vol_name = rdata['Name'].strip('/')
    try:
        mntpoint = volm.driver.path(vol_name)
    except Exception as e:
        return {
            "Err": "Failed to get the volume path for {0}: {1}".format(
                vol_name, str(e)
            )
        }

    if not mntpoint:
        return {
            "Mountpoint": "",
            "Err": "Volume {0} is not mounted".format(vol_name)
        }

    return {
        "Volume": {
            "Name": vol_name,
            "Mountpoint": mntpoint,
            "Status": {},
        },
        "Err": "",
    }


@app.route('/VolumeDriver.List', methods=['POST'])
@normalize
def list_volume():
    """ Routes Docker Volume '/VolumeDriver.List'."""
    volm = app.config['volmer']
    mnt_list = []
    try:
        vol_list = volm.driver.list()
        for volume in vol_list:
            mntpoint = volm.driver.path(volume)
            if not mntpoint:
                mntpoint = "<NOT-MOUNTED>"
            mnt_list += [{
                "Name": volume,
                "Mountpoint": mntpoint,
            }]

    except Exception as e:
        return {
            "Err": "Failed to list the volumes: {0}".format(str(e))
        }

    return {"Volumes": mnt_list, "Err": ""}


@app.route('/VolumeDriver.Capabilities', methods=['POST'])
@normalize
def capabilities_volume():
    """ Routes Docker Volume '/VolumeDriver.Capabilities'."""
    volm = app.config['volmer']
    scope = volm.driver.scope()
    return {"Capabilities": {"Scope": scope}}


def shutdown_server():
    """ Utility method for shutting down the server."""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """ API end point exposed to shutdown the server."""
    shutdown_server()
    return 'Server shutting down...'


class StandaloneApplication(BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def serve_app(app_name):
    config = confight.load_app(app_name)
    plugin_config = config.get("plugin", DEFAULTS["plugin"])
    provisioner_section = plugin_config.pop("provisioner", "provisioner")
    provisioner_config = config.get(
        provisioner_section,
        DEFAULTS[provisioner_section]
    )
    volmer = VolumeManager(provisioner_config)
    app.config['volmer'] = volmer

    try:
        options = plugin_config
        StandaloneApplication(app, options).run()
    finally:
        volmer.cleanup()
