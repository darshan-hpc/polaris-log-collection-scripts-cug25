# Polaris Darshan Log Collection Workflow

The scripts in this directory can be used to automate collection and anonymization of Darshan log data captured on arbitrary systems.

There are 2 key scripts for accomplishing this:
- **darshan-logs-anonymize.py** - a Python script anonymizing the Darshan logs contained in a given input directory in parallel
  - Usage: `python darshan-logs-anonymize.py <input_log_dir> <output_log_dir> <hash_val>`
    - `input_log_dir` - path to directory containing input Darshan logs, typically corresponding to a day of data
    - `output_log_dir` - path to an existing directory to store the new anonymized log files in
    - `hash_val` - random number to use in anonymization hashing
- **darshan-log-collection-workflow.sh** - Bash script managing daily anonymization of a centralized log directory (e.g., used at an HPC facility)
  - Usage: `darshan-log-collection-workflow.sh <input_log_dir> <output_log_dir> <hash_val>`
    - `input_log_dir` - path to directory containing input Darshan logs, typically corresponding to a centralized log directory (organized in "year/month/day" format)
    - `output_log_dir` - path to a directory prefix to store anonymized daily Darshan log tarballs in (in "year/month/day" format)
    - `hash_val` - random number to use in anonymization hashing

Using either of these scripts requires that the `darshan-util` package be installed with bzip2 support. Using Spack, this can be accomplished with the following command: `spack install darshan-util+bzip2`. `darshan-util` binaries need to be included in your `PATH` either by using `spack load darshan-util` or updating `PATH` manually.

The `darshan-log-collection-workflow.sh` script is essentially a more intelligent wrapper over `darshan-logs-anonymize.py` that automates the continuous anonymization of Darshan data captured in a centralized log directory. It is intended for use as part of a regular log collection workflow. This script tracks the most recent day Darshan data was collected and attempts to collect data for all dates following this day when executed.

NOTE: before running `darshan-log-collection-workflow.sh` for the first time, you must initialize a file called `.last_collection` at the root of the provided output log directory. This file should be initialized with a day preceeding the first day intended for collection, with the date expressed in the following format: 'yyyy-mm-dd'. For example, if the input Darshan log collection starts on April 1st, 2025, then the `.last_collection` file could be initialized with a value of '2025-03-31' (i.e., the day preceeding the start of the collection).

NOTE: always use the same hash value when invoking these scripts to ensure anonymization consistently generates the same anonymized values for identical input (e.g., uids).
