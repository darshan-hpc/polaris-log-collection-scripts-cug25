import sys
import pandas as pd

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <2024_jobs_csv> <2025_jobs_csv> <darshan_job_ids_file>")
    sys.exit(1)
jobs_2024_csv = sys.argv[1]
jobs_2025_csv = sys.argv[2]
darshan_jobids_file = sys.argv[3]

# read the input jobid file into a set
darshan_jobids_set = set()
with open(darshan_jobids_file, 'r') as file:
    for line in file:
        darshan_jobids_set.add(line.strip())

# read all 2024 data, and chop off unwanted months (anything before May)
df_2024 = pd.read_csv(jobs_2024_csv)
df_2024['END_MONTH'] = df_2024['END_TIMESTAMP'].apply(lambda x: int(x.split()[0].split('-')[1].lstrip('0')))
df_2024 = df_2024[df_2024['END_MONTH'] >= 5]
df_2024.drop(columns=['END_MONTH'], axis=1, inplace=True)

# read all 2025 data, and chop off unwanted months (anything after Feb)
df_2025 = pd.read_csv(jobs_2025_csv)
df_2025['END_MONTH'] = df_2025['END_TIMESTAMP'].apply(lambda x: int(x.split()[0].split('-')[1].lstrip('0')))
df_2025 = df_2025[df_2025['END_MONTH'] <= 2]
df_2025.drop(columns=['END_MONTH'], axis=1, inplace=True)

# calculate node hours (and other helper vars)
df = pd.concat([df_2024, df_2025])
df['JOBID'] = df['JOB_NAME'].apply(lambda x: x.split('.')[0])
df['NODE_HOURS'] = df['RUNTIME_SECONDS'] * df['NODES_USED'] / 60 / 60
df['MONTH'] = df['END_TIMESTAMP'].apply(lambda x: '-'.join(x.split()[0].split('-')[:2]))

# drop jobs with bogus start times as they blow up the node hour calculation
df = df[df['START_DATE_ID'] != 0]

# group by month, then calculate sum of node hours as well as total job count
month_data = df.groupby('MONTH')['NODE_HOURS'].agg(['sum', 'count'])
month_data.to_csv('all_job_stats.csv')

# again but after filtering to only Darshan recorded jobs
# group by month, then calculate sum of node hours as well as total job count
df = df[df['JOBID'].isin(darshan_jobids_set)]
month_data = df.groupby('MONTH')['NODE_HOURS'].agg(['sum', 'count'])
month_data.to_csv('darshan_job_stats.csv')
