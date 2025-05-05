import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# read in the job data from previous jobs-analyze.py script
all_jobs = pd.read_csv('all_job_stats.csv', index_col='MONTH')
darshan_jobs = pd.read_csv('darshan_job_stats.csv', index_col='MONTH')
pct_df = darshan_jobs / all_jobs

# plot 'sum' against 'MONTH'
ax = pct_df['sum'].plot(marker='o')
ax.xaxis.label.set_visible(False)
ax.set_ylabel('Darshan node-hour coverage', labelpad=15, fontsize=14)
ax.set_xticks(np.arange(len(pct_df.index)))
ax.set_xticklabels(pct_df.index, rotation=45, ha="right")
ax.tick_params(axis='both', labelsize=12)

plt.tight_layout()
plt.show()
