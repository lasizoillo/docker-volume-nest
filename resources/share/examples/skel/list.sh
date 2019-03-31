#!/bin/bash -eu
# List created volumes. Use stderr for errors and stdout to show results
declare base_path=${BASE_PATH:-/mnt/nest}

ls -w 1 -d $base_path | sed "s#${base_path}/##"