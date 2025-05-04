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
sorted_posix_bytes = np.sort(posix_df['total_bytes'])
sorted_stdio_bytes = np.sort(stdio_df['total_bytes'])
sorted_mpiio_bytes = np.sort(mpiio_df['total_bytes'])

# compute and print percentiles for each dataset
percentiles = [50, 75, 90, 99]
posix_percentiles = np.percentile(sorted_posix_bytes, percentiles)
stdio_percentiles = np.percentile(sorted_stdio_bytes, percentiles)
mpiio_percentiles = np.percentile(sorted_mpiio_bytes, percentiles)
for p, posix_val, stdio_val, mpiio_val in zip(percentiles, posix_percentiles, stdio_percentiles, mpiio_percentiles):
    print(f"{p}th percentile:")
    print(f"  POSIX: {posix_val:.2f} bytes")
    print(f"  STDIO: {stdio_val:.2f} bytes")
    print(f"  MPIIO: {mpiio_val:.2f} bytes")

def compute_top_1_percent_sum(sorted_bytes):
    top_1_percent_idx = int(len(sorted_bytes) * 0.99)  # 99th percentile index
    return np.sum(sorted_bytes[top_1_percent_idx:])

# compute and print sums for top 1% of jobs for each dataset
posix_top_1_sum = compute_top_1_percent_sum(sorted_posix_bytes)
stdio_top_1_sum = compute_top_1_percent_sum(sorted_stdio_bytes)
mpiio_top_1_sum = compute_top_1_percent_sum(sorted_mpiio_bytes)
print(f"\nTotal bytes accessed by top 1% of jobs:")
print(f"POSIX: {posix_top_1_sum} bytes (all_jobs = {sum(sorted_posix_bytes)})")
print(f"STDIO: {stdio_top_1_sum} bytes (all jobs = {sum(sorted_stdio_bytes)})")
print(f"MPI-IO: {mpiio_top_1_sum} bytes (all jobs = {sum(sorted_mpiio_bytes)})")

# compute the CDF, the fraction of jobs at each data point
posix_cdf = np.arange(1, len(sorted_posix_bytes) + 1) / len(sorted_posix_bytes)
stdio_cdf = np.arange(1, len(sorted_stdio_bytes) + 1) / len(sorted_stdio_bytes)
mpiio_cdf = np.arange(1, len(sorted_mpiio_bytes) + 1) / len(sorted_mpiio_bytes)

# define xtick values/labels for KiB -> PiB
xticks = [1024**i for i in range(1, 6)]
xtick_labels = ['1 KiB', '1 MiB', '1 GiB', '1 TiB', '1 PiB']

# plot the CDF
plt.figure(figsize=(8, 6))
plt.plot(sorted_posix_bytes, posix_cdf, label='POSIX')
plt.plot(sorted_stdio_bytes, stdio_cdf, label='STDIO')
plt.plot(sorted_mpiio_bytes, mpiio_cdf, label='MPI-IO')
plt.xscale('log')
plt.xticks(xticks, xtick_labels, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Bytes Accessed per Job (log scale)', fontsize=14, labelpad=12)
plt.ylabel('Cumulative Probability', fontsize=14, labelpad=12)
plt.grid(True)
plt.legend(fontsize=14, loc='lower right')
plt.show()
