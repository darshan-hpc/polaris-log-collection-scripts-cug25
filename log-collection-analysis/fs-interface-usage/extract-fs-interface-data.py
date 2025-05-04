import sys
import pandas as pd

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <job_stats_dir>")
    sys.exit(1)
job_stats_dir = sys.argv[1]

interfaces = {'posix': 'POSIX', 'stdio': 'STDIO', 'mpiio': 'MPI-IO'}
fss = {'lus': 'lustre', 'home': 'home', 'scratch': 'local scratch'}

df = pd.DataFrame()

# iterate over each interface-FS combo
for interface in interfaces.keys():
    for fs in fss.keys():
        tmp_df = pd.read_csv(f'{job_stats_dir}/{interface}-{fs}.csv')
        tmp_df = tmp_df[tmp_df['total_bytes'] > 0]
        # calculate some aggregate job statistics
        new_row = pd.DataFrame({
                                'Interface': interfaces[interface],
                                'Storage': fss[fs],
                                'total_jobs': [len(tmp_df)],
                                'total_bytes': [sum(tmp_df['total_bytes'])],
                                'total_files': [sum(tmp_df['total_files'])]
                               })
        df = pd.concat([df, new_row], ignore_index=True)
df.to_csv('fs_interface_usage.csv', index=False)
