# Polaris Darshan Log Collection Workflow

The scripts in this directory can be used to automate collection and anonymization of Darshan log data captured on arbitrary systems.

There are 2 key scripts for accomplishing this:
- **darshan-logs-anonymize.py** - a Python script managing the anonymization of a given input Darshan log directory
  - Usage: ``python darshan-logs-anonymize.py <input_log_dir> <output_log_dir> <hash_val>``
    - `input_log_dir` - path to directory containing input Darshan logs, typically corresponding to a day of data
    - `output_log_dir` - path to an existing directory to store the new anonymized log files in
    - `hash_val` - random number to use in anonymization hashing
- **darshan-log-collection-workflow.sh** - 
