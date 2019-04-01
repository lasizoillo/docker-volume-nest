#!/bin/bash -eu
# Return path where volume should be mounted. Use stderr for errors and stdout to show path where file is mounted
declare base_mnt_dataset=${ZFS_BASE_MNT_DATASET:-/tank/docker-volumes}
declare volname=$1
declare mount_point="${base_mnt_dataset}/${volname}"

mountpoint -q ${mount_point} && echo ${mount_point}