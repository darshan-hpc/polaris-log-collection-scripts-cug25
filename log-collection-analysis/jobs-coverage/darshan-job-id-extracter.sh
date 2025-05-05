#!/bin/bash

# argument checking
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <log_collection_directory>"
    exit 1
fi
log_dir="$1"

find $log_dir -name *.darshan | awk -F/ '{print $NF}' | cut -d- -f 1
