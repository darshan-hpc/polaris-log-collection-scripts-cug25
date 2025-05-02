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

# modules to analyze
modules=("POSIX" "STDIO" "MPI-IO")
module_ids=("posix" "stdio" "mpiio")

# paths to filter by
path_lists=(
	""
	"/lus/ /grand/ /eagle/"
	"/home/"
	"/local/scratch/"
)
path_ids=("all" "lus" "home" "scratch")

# build the input Darshan log manifest
find $log_dir -name *.darshan > log_manifest

# loop over all options
for i in "${!modules[@]}"; do
	for j in "${!path_lists[@]}"; do
		# convert the path_entry string to an array
		IFS=' ' read -r -a path_components <<< "${path_lists[$j]}"

		# build inclusion arguments from lists
		inclusion_args=""
		for part in "${path_components[@]}"; do
			inclusion_args="${inclusion_args} --include_names=^${part}"
		done

		module_id="${module_ids[$i]}"
		path_id="${path_ids[$j]}"
		python -m darshan job_stats --csv --log_paths_file=log_manifest --module=${modules[$i]} $inclusion_args > ${module_id}-${path_id}.csv
	done
done

rm log_manifest
