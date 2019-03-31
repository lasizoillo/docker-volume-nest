#!/bin/bash -eu
# Removes a volume. Use stderr for errors and stdout to show path where volume was mounted
declare base_path=${BASE_PATH:-/mnt/nest}
declare base_mount=${BASE_MOUNT:-/mnt/docker-volume}
declare volname=$1
declare mount_point="${base_mount}/${volname}"

umount $mount_point > /dev/null
rmdir $mount_point

# Destroy your provisioned volume in your alien technology

echo ${mount_point}