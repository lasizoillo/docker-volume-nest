#!/bin/bash -eu
# Removes a volume. Use stderr for errors and stdout to show path where volume was mounted
declare base_dataset=${ZFS_BASE_DATASET:-tank/docker-volumes}
declare default_opts=${ZFS_DEFAULT_OPTS:-""}
declare base_mnt_dataset=${ZFS_BASE_MNT_DATASET:-/tank/docker-volumes}
declare volname=$1
declare mount_point="${base_mnt_dataset}/${volname}"

zfs destroy -R ${base_dataset}/${volname}
echo ${mount_point}