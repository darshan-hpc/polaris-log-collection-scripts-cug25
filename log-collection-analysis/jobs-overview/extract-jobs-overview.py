import sys
import pandas as pd

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <results_dir>")
    sys.exit(1)
results_dir = sys.argv[1]

# load and filter the data
posix_df = pd.read_csv(f'{results_dir}/posix-all.csv', usecols=['log_file', 'total_bytes', 'total_files', 'partial_flag'])
stdio_df = pd.read_csv(f'{results_dir}/stdio-all.csv', usecols=['log_file', 'total_bytes', 'total_files', 'partial_flag'])
mpiio_df = pd.read_csv(f'{results_dir}/mpiio-all.csv', usecols=['log_file', 'total_bytes', 'total_files', 'partial_flag'])

# get rid of erroneous logs with negative MPI-IO counters
mpiio_df = mpiio_df[mpiio_df['total_bytes'] >= 0]

# print overview statistics for each API
print(f'POSIX jobs sum: {len(posix_df)}')
print(f'POSIX bytes sum: {posix_df["total_bytes"].sum()}')
print(f'POSIX files sum: {posix_df["total_files"].sum()}')
print(f'POSIX partial jobs: {len(posix_df[posix_df["partial_flag"] == True])}')
print('\n')
print(f'STDIO jobs sum: {len(stdio_df)}')
print(f'STDIO bytes sum: {stdio_df["total_bytes"].sum()}')
print(f'STDIO files sum: {stdio_df["total_files"].sum()}')
print(f'STDIO partial jobs: {len(stdio_df[stdio_df["partial_flag"] == True])}')
print('\n')
print(f'MPI-IO jobs sum: {len(mpiio_df)}')
print(f'MPI-IO bytes sum: {mpiio_df["total_bytes"].sum()}')
print(f'MPI-IO files sum: {mpiio_df["total_files"].sum()}')
print(f'MPI-IO partial jobs: {len(mpiio_df[mpiio_df["partial_flag"] == True])}')
print('\n')

# calculate total number of jobs doing I/O after combining data from all modules into one dataframe
total_logs = 611606 # 611606 is total number of logs captured from May2024-Feb2025
mpiio_df = mpiio_df.add_suffix('_mpiio')
mpiio_df = mpiio_df.rename(columns={'log_file_mpiio': 'log_file'})
all_df = posix_df.merge(stdio_df, on='log_file', how='outer', suffixes=('_posix', '_stdio')) \
                 .merge(mpiio_df, on='log_file', how='outer')
print(f'total jobs doing I/O: {len(all_df)}')
print(f'total jobs not doing I/O: {total_logs-len(all_df)}')
