#!/bin/bash

# argument checking
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_log_dir> <output_log_dir> <hash_val>"
    exit 1
fi
IN_LOG_DIR_BASE="$1"
OUT_LOG_DIR_BASE="$2"
HASH_VAL="$3"

# make sure directories exist
if [[ ! -d "$IN_LOG_DIR_BASE" ]]; then
    echo "Error: $IN_LOG_DIR_BASE is not a valid directory."
    exit 1
fi
if [[ ! -d "$OUT_LOG_DIR_BASE" ]]; then
    echo "Error: $OUT_LOG_DIR_BASE is not a valid directory."
    exit 1
fi

# make sure the last collection file exists
LAST_COLLECTION_FILE=$OUT_LOG_DIR_BASE/.last_collection
if [ ! -f "$LAST_COLLECTION_FILE" ]; then
    echo "Error: $LAST_COLLECTION_FILE does not exist."
    echo "       This file should be initialized to the a date prior to the first date to be collected."
    exit 1
fi

# terminate on encountered errors
set -e
set -o pipefail

# count of logs that failed anonymization
total_failures=0

# determine last date logs were collected
LAST_COLLECTION_DATE=$(date -d $(cat $LAST_COLLECTION_FILE))
NEXT_COLLECTION_DATE=$(date -d "$LAST_COLLECTION_DATE + 1 day" +"%F")
YESTERDAY=$(date -d "yesterday" +"%F")
while true; do
	# stop when we've processed up through yesterday
	if [[ "$NEXT_COLLECTION_DATE" > "$YESTERDAY" ]]; then
		break;
	fi
	IN_LOG_DIR=$IN_LOG_DIR_BASE/$(date -d $NEXT_COLLECTION_DATE +"%Y/%-m/%-d")
	OUT_LOG_DIR=$OUT_LOG_DIR_BASE/$(date -d $NEXT_COLLECTION_DATE +"%Y/%-m/%-d")
	# skip non-existant or empty directories
	if [ -d $IN_LOG_DIR ] && [ -n "$(find $IN_LOG_DIR -name '*.darshan')" ]; then
		echo "***collecting/anonymizing Darshan logs for $NEXT_COLLECTION_DATE"
		TMP_LOG_DIR=$(mktemp -d)
		output=$(python darshan-logs-anonymize.py $IN_LOG_DIR $TMP_LOG_DIR $HASH_VAL | tee /dev/stderr)
		failures=$(echo "$output" | awk '/failures:/ {print $2}')
		if [[ -n "$failures" ]]; then
			total_failures=$((total_failures + failures))
                fi
		pushd $TMP_LOG_DIR
		tar -czf logs.tar.gz *.darshan
		mkdir -p -m 770 $OUT_LOG_DIR
		mv logs.tar.gz $OUT_LOG_DIR
		popd
		rm -rf $TMP_LOG_DIR
	fi
	# update last_collection file and move to the next date
	echo $NEXT_COLLECTION_DATE > $LAST_COLLECTION_FILE
	NEXT_COLLECTION_DATE=$(date -d "$NEXT_COLLECTION_DATE + 1 day" +"%F")
done

exit $total_failures
