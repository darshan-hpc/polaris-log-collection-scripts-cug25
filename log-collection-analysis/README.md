# Polaris Darshan Log Collection Analysis

The scripts in this directory can be used to process/analyze data in a Darshan log collection, generating overall job statistical summaries and plots.

## Obtaining the Darshan logs

The Polaris Darshan log collection can be downloaded via Globus using the following [LINK](https://app.globus.org/file-manager?origin_id=245b5124-cd81-4381-bc38-243687d95bfd&origin_path=%2F).
This log collection is continuously updated with new logs.

For more details about the log collection, see the documentation on [Zenodo](https://zenodo.org/records/15052604).

Once the log tarballs have been downloaded from Globus, they can be untarred using the `unpack-darshan-logs.sh` script. This script takes a single argument indicating the directory containing the log tarballs and untars each of them in place in this directory hierarchy.

NOTE: The analysis in the CUG'25 paper uses all log data from months 2024/5 - 2025/2 in this continuously updated dataset. If reproducing those results, be sure to restrict analysis to these months only.

## Extracting job statistics for each log

Job statistics for the dataset are extracted using the PyDarshan `job_stats` tool. It is provided as a CLI when installing the PyDarshan package. See the [PyDarshan docs](https://www.mcs.anl.gov/research/projects/darshan/docs/pydarshan/index.html) for details on installing and using PyDarshan. This tool was first made available as part of PyDarshan 3.4.7.0.

With PyDarshan installed, job summary statistics (i.e., the data used for analysis in the CUG'25 paper) can be generated using the `extract-job-stats.sh` script. This script takes a single argument indicating the directory containing the Darshan log data to be analyzed. It generates a set of CSV files containing job statistics across a set of I/O interfaces and storage systems. The CSV files are named as follows: `{interface}-{storage}.csv`

It automatically generates data for the following interfaces:
 - POSIX
 - STDIO
 - MPI-IO

For each of these interfaces, it further generates separate CSV files for each storage type:
 - all: all storage systems (i.e., no filtering of file record data)
 - lus: high-performance Lustre file systems only (e.g., Eagle and Grand Lustre volumes)
 - home: home file system only
 - scratch: node-local scratch file system only

This CSV data can be manually analyzed (e.g., by loading into a pandas DataFrame) or can be analyzed using XXX.

NOTE: individual Darshan logs are typically accounted for in multiple CSV files, as the corresponding jobs typically access data using multiple interfaces and/or storage systems. Data is organized like this to better understand the extent of the usage of different interfaces and storage systems, which is not clear from the aggregate statistics (i.e., the "all" category).

NOTE: the `extract-job-stats.sh` script should be modified when used on systems besides Polaris to account for different file system mount points to analyze (e.g., `/home`, `/lus`, etc.).

## Analyzing the logs

The following subdirectories contain documentation scripts used for generating data and plots used in the paper:

- [jobs-overview](jobs-overview) - Overall job statistics for each interface (used for **Table 2**)
- [jobs-cdfs](jobs-cdfs) - CDF plots of bytes accessed, files accessed, and observed performance for each interface (used for **Figure 4**)
- [fs-interface-usage](fs-interface-usage) - Bar plots of storage system usage in terms of jobs and bytes for each interface (used for **Figure 5**)
- [case-study-1](case-study-1) - Steps for detecting and analyzing the job in Case Study 1 (**Section 4.3.1**, **Figure 7**)
