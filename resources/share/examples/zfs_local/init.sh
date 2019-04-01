#!/bin/bash -eu
# Init your volume infraestructure. Stderr and stdout are ignored
declare base_dataset=${ZFS_BASE_DATASET:-tank/docker-volumes}
declare base_mnt_dataset=${ZFS_BASE_MNT_DATASET:-/tank/docker-volumes}
declare default_opts=${ZFS_DEFAULT_INIT_OPTS:-"-o sharenfs=on -o mountpoint=${base_mnt_dataset}"}

zfs create -p ${base_dataset} ${default_opts}