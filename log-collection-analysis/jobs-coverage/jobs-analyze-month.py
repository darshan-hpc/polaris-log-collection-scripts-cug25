import sys
import pandas as pd

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} <jobs_csv> <month> <darshan_job_ids_file>")
    sys.exit(1)
jobs_csv = sys.argv[1]
month = sys.argv[2]
darshan_jobids_file = sys.argv[3]

# read the input jobid file into a set
darshan_jobids_set = set()
with open(darshan_jobids_file, 'r') as file:
    for line in file:
        darshan_jobids_set.add(line.strip())

# read in the jobs info and filter by desired month
df = pd.read_csv(jobs_csv)
df['END_MONTH'] = df['END_TIMESTAMP'].apply(lambda x: int(x.split()[0].split('-')[1].lstrip('0')))
df = df[df['END_MONTH'] == int(month)]

# calculate node hours (and other helper vars)
df['JOBID'] = df['JOB_NAME'].apply(lambda x: x.split('.')[0])
df['NODE_HOURS'] = df['RUNTIME_SECONDS'] * df['NODES_USED'] / 60 / 60
df['MONTH'] = df['END_TIMESTAMP'].apply(lambda x: '-'.join(x.split()[0].split('-')[:2]))

# drop jobs with bogus start times as they blow up the node hour calculation
df = df[df['START_DATE_ID'] != 0]

# group by project, then calculate sum of node hours as well as total job count
proj_data = df.groupby('PROJECT_NAME_GENID')['NODE_HOURS'].agg(['sum', 'count'])
proj_data.to_csv(f'all_job_stats-{month}.csv')

# again but after filtering to only Darshan recorded jobs
# group by project, then calculate sum of node hours as well as total job count
df = df[df['JOBID'].isin(darshan_jobids_set)]
proj_data = df.groupby('PROJECT_NAME_GENID')['NODE_HOURS'].agg(['sum', 'count'])
proj_data.to_csv(f'darshan_job_stats-{month}.csv')
