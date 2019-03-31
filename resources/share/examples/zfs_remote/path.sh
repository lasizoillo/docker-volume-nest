#!/bin/bash -eu
# Return path where volume should be mounted. Use stderr for errors and stdout to show path where file is mounted
declare base_mount=${BASE_MOUNT:-/mnt/docker-volume}
declare volname=$1
declare mount_point="${base_mount}/${volname}"

echo ${mount_point}