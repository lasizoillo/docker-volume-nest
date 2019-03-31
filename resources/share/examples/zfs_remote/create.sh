#!/bin/bash -eu
# Create a volume. Stderr and stdout are ignored
# options var are lines with format: "name=value"
declare base_path=${BASE_PATH:-/mnt/nest}
declare volname=$1
declare options=$2

echo "Do usable things here: useful-command create ${base_path}/${volname} -o ..."