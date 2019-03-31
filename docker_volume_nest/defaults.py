DEFAULTS = {
    "plugin": {
        "bind": "unix:/run/docker/plugins/nest.sock",
    },
    "provisioner": {
        "tmpl": {
            "dataset": {
                "body": "{{dataset_root}}/{{volname}}",
            },
            "cmd_options": {
                "body": "{% for k,v in options.items() %} -o k=v {% endfor %}",
                "params": ["options"]
            },
            "mountpoint": {
                "body": "{{mount_root}}/{{volname}}"
            }
        },
        "cfg": {
            "dataset_root": "tank/docker-volumes",
            "mount_root": "tank/docker-volumes",
            "default_options": {
            },
            "default_init_options": {
                "sharenfs": "on"
            },
            "nfs_server": "localhost",
            "nfs_options": "-o hard,nolock"
        },
        "cmd": {
            "init": "zfs create -p {{dataset()}} {{cmd_options(default_init_options)}}",
            "create": "zfs create -p {{dataset()}} {{cmd_options(options)}} {{cmd_options(default_options)}}",
            "list": "zfs list -r -t filesystem -o name -H {{dataset()}}",
            "path": "{{mountpoint()}}",
            "remove": "echo zfs destroy -r {{dataset()}}",
            "mount": "",
            "umount": "",
        }
    },
    "provisioner_remote": {
        "tmpl": {
            "dataset": {
                "body": "{{dataset_root}}/{{volname}}",
            },
            "cmd_options": {
                "body": "{% for k,v in options.items() %} -o k=v {% endfor %}",
                "params": ["options"]
            },
            "mountpoint": {
                "body": "{{mount_root}}/{{volname}}"
            }
        },
        "cfg": {
            "dataset_root": "tank/docker-volumes",
            "mount_root": "/mnt/docker-volumes",
            "default_options": {
            },
            "default_init_options": {
                "sharenfs": "on"
            },
            "nfs_server": "localhost",
            "nfs_options": "-o hard,nolock"
        },
        "cmd": {
            "init": "ssh {{nfs_server}} zfs create -p {{dataset()}} {{cmd_options(default_init_options)}}",
            "create": "ssh {{nfs_server}} zfs create -p {{dataset()}} {{cmd_options(options)}} {{cmd_options(default_options)}}",
            "list": "showmount --no-headers -e {{nfs_ser",
            "path": "{{mountpoint()}}",
            "remove": "echo zfs destroy -r {{dataset()}}",
            "mount": "mkdir -p mountpoint(); mount {{nfs_options}}:/{{dataset()}} {{mountpoint()}}",
            "umount": "umount {{mountpoint()}}; rmdir {{mountpoint()}}",
        }
    }
}