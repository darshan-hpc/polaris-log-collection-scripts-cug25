import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <job_stats_dir>")
    sys.exit(1)
job_stats_dir = sys.argv[1]

# load data
posix_df = pd.read_csv(f'{job_stats_dir}/posix-all.csv')
stdio_df = pd.read_csv(f'{job_stats_dir}/stdio-all.csv')
mpiio_df = pd.read_csv(f'{job_stats_dir}/mpiio-all.csv')

# filter and sort the data in ascending order
posix_df = posix_df[posix_df['total_bytes'] > 0]
stdio_df = stdio_df[stdio_df['total_bytes'] > 0]
mpiio_df = mpiio_df[mpiio_df['total_bytes'] > 0]
sorted_posix_perf = np.sort(posix_df['perf_by_slowest'])
sorted_stdio_perf = np.sort(stdio_df['perf_by_slowest'])
sorted_mpiio_perf = np.sort(mpiio_df['perf_by_slowest'])

# compute and print percentiles for each dataset
percentiles = [50, 75, 90, 99]
posix_percentiles = np.percentile(sorted_posix_perf, percentiles)
stdio_percentiles = np.percentile(sorted_stdio_perf, percentiles)
mpiio_percentiles = np.percentile(sorted_mpiio_perf, percentiles)
for p, posix_val, stdio_val, mpiio_val in zip(percentiles, posix_percentiles, stdio_percentiles, mpiio_percentiles):
    print(f"{p}th percentile:")
    print(f"  POSIX: {posix_val:.2f} bytes/s")
    print(f"  STDIO: {stdio_val:.2f} bytes/s")
    print(f"  MPIIO: {mpiio_val:.2f} bytes/s")

# compute the CDF, the fraction of jobs at each data point
posix_cdf = np.arange(1, len(sorted_posix_perf) + 1) / len(sorted_posix_perf)
stdio_cdf = np.arange(1, len(sorted_stdio_perf) + 1) / len(sorted_stdio_perf)
mpiio_cdf = np.arange(1, len(sorted_mpiio_perf) + 1) / len(sorted_mpiio_perf)

# define xtick values/labels for KiB/s -> TiB/s
xticks = [1024**i for i in range(1, 5)]
xtick_labels = ['1 KiB/s', '1 MiB/s', '1 GiB/s', '1 TiB/s']

# plot the CDF
plt.figure(figsize=(8, 6))
plt.plot(sorted_posix_perf, posix_cdf, label='POSIX')
plt.plot(sorted_stdio_perf, stdio_cdf, label='STDIO')
plt.plot(sorted_mpiio_perf, mpiio_cdf, label='MPI-IO')
plt.xscale('log')
plt.xticks(xticks, xtick_labels, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Performance per Job (log scale)', fontsize=14, labelpad=12)
plt.ylabel('Cumulative Probability', fontsize=14, labelpad=12)
plt.grid(True)
plt.legend(fontsize=14, loc='lower right')
plt.show()
