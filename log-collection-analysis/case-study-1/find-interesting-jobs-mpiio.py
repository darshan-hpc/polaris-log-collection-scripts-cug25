import sys
import pandas as pd

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <job_stats_dir>")
    sys.exit(1)
job_stats_dir = sys.argv[1]

# read input MPI-IO data
mpiio_df = pd.read_csv(f'{job_stats_dir}/mpiio-all.csv')
 
# filter out jobs doing small amounts of I/O (less than 1 GiB)
mpiio_df = mpiio_df[mpiio_df['total_bytes'] > (1024**3)]

# re-sort data to be in ascending performance (default for job_stats is descending total_bytes)
mpiio_df = mpiio_df.sort_values(by='perf_by_slowest')

# print out 10 lowest performing jobs to inspect manually
print(mpiio_df.head(10).to_string())
