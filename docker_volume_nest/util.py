import subprocess
import shlex
import logging


logger = logging.getLogger(__name__)


def exec_command(config, name, *args):
    if name in config.get("cmd", {}):
        cmd_args = shlex.split(config["cmd"][name]) + list(args)
        ret = subprocess.Popen(
            args=cmd_args, env=config.get("environment", {}),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = ret.communicate()
        logger.info("STDOUT({}, {}):\n{}".format(name, args, stdout))
        logger.info("STDERR({}, {}):\n{}".format(name, args, stderr))
        if ret.returncode != 0:
            raise Exception(
                "Command {} failed with status {}:\nOUT={}\nERR={}".format(
                    name, ret.returncode, stdout, stderr
                )
            )
        return stdout.decode("utf-8").strip()
    return ""
