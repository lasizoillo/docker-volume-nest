#!/bin/bash -eu
# Create a volume. Stderr and stdout are ignored
# options var are lines with format: "name=value"
declare base_dataset=${ZFS_BASE_DATASET:-tank/docker-volumes}
declare default_opts=${ZFS_DEFAULT_OPTS:-""}
declare volname=$1
declare options=$2

declare opts=$(cat <(echo -e "$options") | sed 's#^\(.\+\)#-o \1#' | tr -s '\n' ' ')

zfs create -p "${base_dataset}/${volname}" ${default_opts} $opts