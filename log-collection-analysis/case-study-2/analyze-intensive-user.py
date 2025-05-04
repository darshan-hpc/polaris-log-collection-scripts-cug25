import sys
import pandas as pd

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <job_stats_dir>")
    sys.exit(1)
job_stats_dir = sys.argv[1]

stdio_df = pd.read_csv(f'{job_stats_dir}/stdio-all.csv')

# print overall STDIO stats along with aggregate stats for user identified in this case study
print(f'total STDIO jobs: {len(stdio_df)}')
print(f'total STDIO job PiB: {sum(stdio_df["total_bytes"])/(1024**5)}')
print(f'total STDIO job files: {sum(stdio_df["total_files"])}')
interesting_user_df = stdio_df[stdio_df['uid'] == 387797653]
print(f'interesting user STDIO jobs: {len(interesting_user_df)}')
print(f'interesting user STDIO job PiB: {sum(interesting_user_df["total_bytes"])/(1024**5)}')
print(f'interesting user STDIO job files: {sum(interesting_user_df["total_files"])}')
