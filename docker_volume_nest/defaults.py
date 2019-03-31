__all__ = ["DEFAULTS"]


def cmd(name):
    return "/usr/share/docker_volume_nest/examples/skel/{}.sh".format(
        name
    )


DEFAULTS = {
    "service": {
        "bind": "unix:/run/docker/plugins/nest.sock",
    },
    "environment": {
    },
    "cmd": {
        "init": cmd("init"),
        "create": cmd("create"),
        "list": cmd("list"),
        "path": cmd("path"),
        "remove": cmd("remove"),
        "mount": cmd("mount"),
        "umount": cmd("umount"),
        "scope": cmd("scope"),
    },
}
