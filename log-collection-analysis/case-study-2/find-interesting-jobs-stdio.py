import sys
import pandas as pd

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <job_stats_dir>")
    sys.exit(1)
job_stats_dir = sys.argv[1]

stdio_df = pd.read_csv(f'{job_stats_dir}/stdio-all.csv')
stdio_df = stdio_df[stdio_df['total_bytes'] > 0]

# print out 10 highest intensity jobs (in terms of total bytes) to inspect manually
print(stdio_df.head(10).to_string())
