import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <fs_api_usage_csv>")
    sys.exit(1)

df = pd.read_csv(sys.argv[1])

# reorganize input data with storage systems as rows and APIs as columns
df_pivot = df.pivot(index="Storage", columns="API", values="total_bytes")
df_pivot = df_pivot[["POSIX", "STDIO", "MPI-IO"]].reindex(["lustre", "home", "local scratch"])
fses = df_pivot.index
apis = df_pivot.columns

# define x-tick values and labels
xtick_values = [2**30, 2**40, 2**50]
xtick_labels = ['1 GiB', '1 TiB', '1 PiB']
xtick_map = dict(zip(xtick_values, xtick_labels))

# function to format annotation in terms of the closest lower unit
def format_annotation(value):
    lower_ticks = [tick for tick in xtick_values if tick <= value]
    if not lower_ticks:
        return f"{value:,}"  # Fallback if below GiB
    closest_tick = max(lower_ticks)  # Largest tick ≤ value
    unit_label = xtick_map[closest_tick]
    formatted_value = value / closest_tick  # Convert to unit
    return f"{formatted_value:.1f} {unit_label.split()[1]}"

# plot APIs for each set of storage systems as horizontal bars
plt.figure(figsize=(8, 6))
ax = plt.gca()
bar_height = 0.2
y = np.arange(len(fses))
for i, api in enumerate(apis):
    offset = (i - 1) * bar_height
    bars = ax.barh(y + offset, df_pivot[api], height=bar_height, label=api, edgecolor='black')

    # annotate each bar in terms of the closest lower xtick
    for bar in bars:
        width = bar.get_width()
        ax.text(width * 1.1, bar.get_y() + bar.get_height() / 2, format_annotation(width),
                ha='left', va='center', fontsize=10)

# plot formatting
ax.set_xscale('log')
ax.set_xticks(xtick_values)
ax.set_xticklabels(xtick_labels)
ax.xaxis.set_major_locator(ticker.FixedLocator(xtick_values))
ax.xaxis.set_minor_locator(ticker.NullLocator())
ax.set_yticks(y)
ax.set_yticklabels(fses)
ax.set_xlabel("Number of Bytes (log scale)", fontsize=14)
ax.set_ylabel("Storage System", fontsize=14)
ax.legend(loc="best", fontsize=14, title_fontsize=14)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# adjust limits to prevent annotation cut-off
ax.set_xlim(min(xtick_values) * 0.9, max(xtick_values) * 50)

plt.xticks(fontsize=13)
plt.yticks(fontsize=13)
plt.tight_layout()
plt.show()
