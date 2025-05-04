import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <results_dir>")
    sys.exit(1)
results_dir = sys.argv[1]

# load data
posix_df = pd.read_csv(f'{results_dir}/posix-all.csv')
stdio_df = pd.read_csv(f'{results_dir}/stdio-all.csv')
mpiio_df = pd.read_csv(f'{results_dir}/mpiio-all.csv')

# filter and sort the data in ascending order
posix_df = posix_df[posix_df['total_files'] > 0]
stdio_df = stdio_df[stdio_df['total_files'] > 0]
mpiio_df = mpiio_df[mpiio_df['total_files'] > 0]
sorted_posix_files = np.sort(posix_df['total_files'])
sorted_stdio_files = np.sort(stdio_df['total_files'])
sorted_mpiio_files = np.sort(mpiio_df['total_files'])

# compute and print percentiles for each dataset
percentiles = [50, 75, 90, 99]
posix_percentiles = np.percentile(sorted_posix_files, percentiles)
stdio_percentiles = np.percentile(sorted_stdio_files, percentiles)
mpiio_percentiles = np.percentile(sorted_mpiio_files, percentiles)
for p, posix_val, stdio_val, mpiio_val in zip(percentiles, posix_percentiles, stdio_percentiles, mpiio_percentiles):
    print(f"{p}th percentile:")
    print(f"  POSIX: {posix_val:.2f} files")
    print(f"  STDIO: {stdio_val:.2f} files")
    print(f"  MPIIO: {mpiio_val:.2f} files")

# compute the CDF, the fraction of jobs at each data point
posix_cdf = np.arange(1, len(sorted_posix_files) + 1) / len(sorted_posix_files)
stdio_cdf = np.arange(1, len(sorted_stdio_files) + 1) / len(sorted_stdio_files)
mpiio_cdf = np.arange(1, len(sorted_mpiio_files) + 1) / len(sorted_mpiio_files)

# plot the CDF
plt.figure(figsize=(8, 6))
plt.plot(sorted_posix_files, posix_cdf, label='POSIX')
plt.plot(sorted_stdio_files, stdio_cdf, label='STDIO')
plt.plot(sorted_mpiio_files, mpiio_cdf, label='MPI-IO')
plt.xscale('log')
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Files Accessed per Job (log scale)', fontsize=14, labelpad=12)
plt.ylabel('Cumulative Probability', fontsize=14, labelpad=12)
plt.grid(True)
plt.legend(fontsize=14, loc='lower right')
plt.minorticks_off()
plt.show()
