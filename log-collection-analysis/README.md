# Polaris Darshan Log Collection Analysis

This repository contains various scripts and documentation for reproducing results from the Polaris log collection paper presented at CUG'25.

## Obtaining the Darshan logs

The Polaris Darshan log collection can be downloaded via Globus using the following [LINK](https://app.globus.org/file-manager?origin_id=245b5124-cd81-4381-bc38-243687d95bfd&origin_path=%2F).
This log collection is continuously updated with new logs.

For more details about the log collection, see the documentation on [Zenodo](https://zenodo.org/records/15052604).

Once the log tarballs have been downloaded from Globus, they can be untarred using the `data_collection/unpack-darshan-logs.sh` script. This script takes a single argument indicating the directory containing the log tarballs and untars each of them in place in this directory hierarchy.

NOTE: The analysis in the CUG'25 paper uses all log data from months 2024/5 - 2025/2 in this continuously updated dataset. If reproducing those results, be sure to restrict analysis to these months only.

## Extracting job statistics for each log

Job statistics for the dataset are extracted using the PyDarshan `job_stats` tool. It is provided as a CLI when installing the PyDarshan package. See the [PyDarshan docs](https://www.mcs.anl.gov/research/projects/darshan/docs/pydarshan/index.html) for details on installing and using PyDarshan. This tool was first made available as part of PyDarshan 3.4.7.0.

With PyDarshan installed, all job data used for the CUG'25 paper can be generated using the `data_collection/extract-job-stats.sh` script. This script takes a single argument indicating the directory containing all Darshan log data to be analyzed. It generates a set of CSV files containing job statistics across a set of I/O interfaces and storage systems. The CSV files are named as follows: `{inteface}-{storage}.csv`

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

NOTE: individual Darshan logs are typically accounted for in multiple CSV files, as the corresponding jobs typically access data using multiple APIs and/or storage systems. Data is organized like this to better understand the extent of the usage of different APIs and storage systems, which is not clear from the aggregate statistics (i.e., the "all" category).
