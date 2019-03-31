import logging
import os
import os.path

from .util import exec_command

log = logging.getLogger(__name__)

NOT_MOUNTED = '<Not Mounted>'


class HookedDriver(object):
    """
    Use external commands to implement your plugin
    """

    def __init__(self, config):
        self.config = config
        cmd_ret = exec_command(config, "init")
        log.info("Init() => {}".format(cmd_ret))

    def create(self, volname, options):
        if not volname:
            raise ValueError("volname is mandatory")
        str_opts = "\n".join([
            "{}={}".format(k, v)
            for k, v in options.items()
        ])
        cmd_ret = exec_command(self.config, "create", volname, str_opts)
        log.info("Create(volname={}, options={}) => {}".format(
            volname, options, cmd_ret
        ))
        return ""

    def list(self):
        cmd_ret = exec_command(self.config, "list")
        log.info("List() => {}".format(cmd_ret))
        return cmd_ret.splitlines()

    def path(self, volname):
        if not volname:
            raise ValueError("volname is mandatory")
        cmd_ret = exec_command(self.config, "path", volname)
        log.info("Path(volname={}) => {}".format(
            volname, cmd_ret
        ))
        return cmd_ret

    def remove(self, volname):
        if not volname:
            raise ValueError("volname is mandatory")
        cmd_ret = exec_command(self.config, "remove", volname)
        log.info("Remove(volname={}) => {}".format(volname, cmd_ret))
        return cmd_ret

    def mount(self, volname):
        if not volname:
            raise ValueError("volname is mandatory")
        cmd_ret = exec_command(self.config, "mount", volname)
        log.info("Mount(volname={}) => {}".format(volname, cmd_ret))
        return cmd_ret

    def umount(self, volname):
        if not volname:
            raise ValueError("volname is mandatory")
        cmd_ret = exec_command(self.config, "umount", volname)
        log.info("Umount(volname={}) => {}".format(volname, cmd_ret))
        return cmd_ret

    def cleanup(self):
        # TODO: Implement command
        pass

    def scope(self):
        cmd_ret = exec_command(self.config, "scope")
        log.info("Scope() => {}".format(cmd_ret))
        return cmd_ret
