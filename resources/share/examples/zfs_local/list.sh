#!/bin/bash -eu
# List created volumes. Use stderr for errors and stdout to show results
declare base_mnt_dataset=${ZFS_BASE_MNT_DATASET:-/tank/docker-volumes}

ls -w 1 -d ${base_mnt_dataset}/* | sed "s#${base_mnt_dataset}/##"