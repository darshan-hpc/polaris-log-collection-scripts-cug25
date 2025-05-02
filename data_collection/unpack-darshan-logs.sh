#!/bin/bash

# argument checking
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <log_collection_directory>"
    exit 1
fi
log_dir="$1"

# make sure directory exists
if [[ ! -d "$log_dir" ]]; then
    echo "Error: $log_dir is not a valid directory."
    exit 1
fi

# untar Darshan logs in parallel
find "$log_dir" -name "logs.tar.gz" -print0 |\
	xargs -0 -P 16 -I{} sh -c \
	'echo "Extracting: {}"; cd "$(dirname "{}")" && tar -xzf logs.tar.gz && echo "Done: {}"'
