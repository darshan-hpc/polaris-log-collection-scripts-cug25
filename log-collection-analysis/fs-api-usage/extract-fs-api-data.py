import sys
import pandas as pd

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <results_dir>")
    sys.exit(1)
results_dir = sys.argv[1]

apis = {'posix': 'POSIX', 'stdio': 'STDIO', 'mpiio': 'MPI-IO'}
fss = {'lus': 'lustre', 'home': 'home', 'scratch': 'local scratch'}

df = pd.DataFrame()

# iterate over each API-FS combo
for api in apis.keys():
    for fs in fss.keys():
        tmp_df = pd.read_csv(f'{results_dir}/{api}-{fs}.csv')
        tmp_df = tmp_df[tmp_df['total_bytes'] > 0]
        # calculate some aggregate job statistics
        new_row = pd.DataFrame({
                                'API': apis[api],
                                'Storage': fss[fs],
                                'total_jobs': [len(tmp_df)],
                                'total_bytes': [sum(tmp_df['total_bytes'])],
                                'total_files': [sum(tmp_df['total_files'])]
                               })
        df = pd.concat([df, new_row], ignore_index=True)
df.to_csv('fs_api_usage.csv', index=False)
