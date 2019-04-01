#!/bin/bash -eu
# Unmounts a volume. Use stderr or stdout for errors, stdout is ignored
declare base_mount=${BASE_MOUNT:-/mnt/docker-volume}
declare volname=$1
declare mount_point="${base_mount}/${volname}"

# No problem with mounted volumes