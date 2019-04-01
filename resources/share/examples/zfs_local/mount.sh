#!/bin/bash -eu
# Mount volumes. Use stderr for errors and stdout to show path where file is mounted
declare base_mnt_dataset=${ZFS_BASE_MNT_DATASET:-/tank/docker-volumes}
declare volname=$1
declare mount_point="${base_mnt_dataset}/${volname}"

# Nothing to do, datasetes mounts are automatic
echo ${mount_point}