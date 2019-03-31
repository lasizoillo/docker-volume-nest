import logging
import os
import os.path

from jinja2 import Template

log = logging.getLogger(__name__)

NOT_MOUNTED = '<Not Mounted>'


class HookedDriver(object):
    """
    Generate commands for provision volumes from jinja2 templates in a config
    file
    """

    def __init__(self, config):
        self.config = config
        # TODO: Create base dataset recursively
        # TODO: Grant creation
        self.cfg = config.get("cfg", {})
        self.base = self.cfg.get("dataset_root")
        log.info("Using {0} as the base".format(self.base))
        self.mount_point = self.cfg.get("mount_root")
        self.vol_dict = {}

        self._generate_templates()

    def _generate_templates(self):
        templates = {}
        template = ""
        for k, v in self.config.get("tmpl", {}).items():
            macro_param = v.get("params", [])
            template += "{%- macro "
            template += k
            template += "(" + ",".join(macro_param) + ") -%}"
            template += v.get("body", "")
            template += "{%- endmacro -%}"

        for k, v in self.config.get("cmd").items():
            t = Template(template + v)
            t.globals = self.config.get("cfg", {})
            templates[k] = t
        self.templates = templates

    def create(self, volname, options):
        # TODO: Create dataset for volname
        if not volname:
            raise ValueError("volname is mandatory")
        cmd = self.templates["create"].render(options=options, volname=volname)
        log.info("Create => {}".format(cmd))

        path = os.path.join(self.base, volname)
        rpath = os.path.join(self.mount_point, volname)

        self.vol_dict[volname] = {'Local': path, 'Remote': rpath}

    def list(self):
        # TODO: List datasets names
        cmd = self.templates["list"].render()
        log.info("List => {}".format(cmd))

        return []

    def path(self, volname):
        if self.vol_dict[volname]['Remote'] == NOT_MOUNTED:
            log.error('Volume {0} is not mounted'.format(volname))
            return None
        log.info("Path => {}".format(self.vol_dict[volname]['Remote']))
        cmd = self.templates["path"].render(volname=volname)
        log.info("Path(tmpl) => {}".format(cmd))
        return self.vol_dict[volname]['Remote']

    def remove(self, volname):
        # TODO: Destroy dataset
        try:
            self.umount(volname)
        except Exception as e:
            raise e
        cmd = self.templates["remove"].render(volname=volname)
        log.info("Remove => {}".format(cmd))

    def mount(self, volname):
        # TODO: Mount dataset via nfs
        # local_path = self.vol_dict[volname]['Local']
        remote_path = self.vol_dict[volname]['Remote']
        cmd = self.templates["mount"].render(volname=volname)
        log.info("Mount => {}".format(cmd))
        return remote_path

    def umount(self, volname):
        # TODO: Unmount dataset via nfs
        cmd = self.templates["umount"].render(volname=volname)
        log.info("Umount => {}".format(cmd))
        self.vol_dict[volname]['Remote'] = NOT_MOUNTED

    def cleanup(self):
        # TODO: Unmount nfs volume
        # TODO: Remove mount dir
        pass

    def scope(self):
        return "global"
