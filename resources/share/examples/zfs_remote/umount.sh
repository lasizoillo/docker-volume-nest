#!/bin/bash -eu
# Unmounts a volume. Use stderr or stdout for errors, stdout is ignored
declare base_mount=${BASE_MOUNT:-/mnt/docker-volume}
declare volname=$1
declare mount_point="${base_mount}/${volname}"

umount $mount_point > /dev/null
rmdir $mount_point

echo ${mount_point}