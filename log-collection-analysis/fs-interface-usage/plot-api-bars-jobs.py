import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <fs_api_usage_csv>")
    sys.exit(1)

df = pd.read_csv(sys.argv[1])

# reorganize input data with storage systems as rows and APIs as columns
df_pivot = df.pivot(index="Storage", columns="API", values="total_jobs")
df_pivot = df_pivot[["POSIX", "STDIO", "MPI-IO"]].reindex(["lustre", "home", "local scratch"])
fses = df_pivot.index
apis = df_pivot.columns

# plot APIs for each set of storage systems as horizontal bars
plt.figure(figsize=(8, 6))
ax = plt.gca()
bar_height = 0.2  
y = np.arange(len(fses))
for i, api in enumerate(apis):
    offset = (i - 1) * bar_height  
    bars = ax.barh(y + offset, df_pivot[api], height=bar_height, label=api, edgecolor='black')
    
    # annotate each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 5000, bar.get_y() + bar.get_height()/2 - .01, f'{width:,}', 
                ha='left', va='center', fontsize=10)

# plot formatting
ax.set_yticks(y)
ax.set_yticklabels(fses)
ax.set_xlabel("Number of Jobs", fontsize=14)
ax.set_ylabel("Storage System", fontsize=14)
ax.legend(loc="best", fontsize=14, title_fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.get_xaxis().set_major_formatter(
    ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

# adjust limits to prevent annotation cut-off
ax.set_xlim(0, df_pivot.values.max() * 1.1)  

plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.tight_layout()
plt.show()
