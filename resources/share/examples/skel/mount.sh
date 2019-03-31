#!/bin/bash -eu
# Mount volumes. Use stderr for errors and stdout to show path where file is mounted
declare base_path=${BASE_PATH:-/mnt/nest}
declare base_mount=${BASE_MOUNT:-/mnt/docker-volume}
declare volname=$1
declare mount_point="${base_mount}/${volname}"

mount -t alien_tech -o dataset="${base_path}/${volname}" ${mount_point} > /dev/null
echo ${mount_point}