import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import string

# percentage of total node-hours to print as individual projects
THRESHOLD=.9

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <projects_csv> <projects_darshan_csv>")
    sys.exit(1)
projects_csv = sys.argv[1]
projects_darshan_csv = sys.argv[2]

# read in projects info and Darshan covered projects info
all_projects_sum_df = pd.read_csv(projects_csv, index_col='PROJECT_NAME_GENID').sort_values('sum', ascending=False)
darshan_projects_sum_df = pd.read_csv(projects_darshan_csv, index_col='PROJECT_NAME_GENID')
# re-index Darshan data to have same indices as all projects data
darshan_projects_sum_df = darshan_projects_sum_df.reindex(all_projects_sum_df.index, fill_value=0)
diff_sum_df = all_projects_sum_df - darshan_projects_sum_df

instrumented_df = darshan_projects_sum_df.drop(columns=['count'])
uninstrumented_df = diff_sum_df.drop(columns=['count'])
instrumented_df = instrumented_df.rename(columns={'sum': 'NODE_HOURS'})
instrumented_df.index.name = 'PROJECT'
uninstrumented_df = uninstrumented_df.rename(columns={'sum': 'NODE_HOURS'})
uninstrumented_df.index.name = 'PROJECT'

print(f'instrumented total node-hours: {instrumented_df["NODE_HOURS"].sum()}')
print(f'uninstrumented total node-hours: {uninstrumented_df["NODE_HOURS"].sum()}')

def rename_top_projects(index):
    """
    Rename project indices to Proj 1, Proj 2, ..., while keeping 'Other' unchanged.
    """
    return {old_name: f"Proj {i+1}" for i, old_name in enumerate(index)}

def aggregate_other_projects(df, top_N):
    # Sum the top N projects and aggregate the rest into "Other"
    top_projects = df.head(top_N)['NODE_HOURS']
    other_projects = df.tail(len(df) - top_N)['NODE_HOURS'].sum()

    return top_projects, other_projects

def determine_top_N(instrumented_df, uninstrumented_df, threshold=0.9):
    """
    Determine the number of top projects (`top_N`) that collectively exceed `threshold` 
    (e.g., 90%) of the total node hours across both instrumented and uninstrumented data.
    """
    # Compute total node hours per project
    total_node_hours_per_project = instrumented_df['NODE_HOURS'].add(uninstrumented_df['NODE_HOURS'], fill_value=0)
    
    # Sort projects by total node hours (descending)
    total_node_hours_per_project = total_node_hours_per_project.sort_values(ascending=False)
    
    # Compute cumulative sum and determine `top_N`
    cumulative_sum = total_node_hours_per_project.cumsum()
    total_node_hours = total_node_hours_per_project.sum()
    
    # Find the smallest N where cumulative sum exceeds 90% of total node hours
    top_N = (cumulative_sum <= threshold * total_node_hours).sum() + 1  # +1 to ensure we include the last needed project
    
    return top_N

# Determine top_N dynamically
top_N = determine_top_N(instrumented_df, uninstrumented_df, threshold=THRESHOLD)

# Count the number of projects in "Other"
num_other_projects = len(instrumented_df) - top_N

# Aggregate top N instrumented and uninstrumented projects
top_instrumented, other_instrumented = aggregate_other_projects(instrumented_df, top_N)
top_uninstrumented, other_uninstrumented = aggregate_other_projects(uninstrumented_df, top_N)

rename_mapping = rename_top_projects(top_instrumented.index)
top_instrumented = top_instrumented.rename(index=rename_mapping)
top_uninstrumented = top_uninstrumented.rename(index=rename_mapping)

# Create a new dataframe for plotting
top_projects_df = pd.DataFrame({
    'Instrumented': top_instrumented.values,
    'Uninstrumented': top_uninstrumented.values
}, index=top_instrumented.index)

# Add the "Other" category at the end
other_category = pd.Series([other_instrumented, other_uninstrumented], 
                           index=['Instrumented', 'Uninstrumented'], 
                           name='Other')

# Concatenate the "Other" category to the top_projects_df
top_projects_df = pd.concat([top_projects_df, other_category.to_frame().T])

plt.figure(figsize=(10, 10))
ax = plt.gca()

# plot stacked bar chart of instrumented/uninstrumented node-hours for each project
top_projects_df.plot(kind='barh', stacked=True, ax=ax, color=["blue", "red"])

# annotate with an arrow indicating number of "Other" projects
other_index = len(top_projects_df) - 1  # Since "Other" is added last
other_bar_value = top_projects_df.iloc[other_index].sum()  # Total node-hours for "Other"
ax.annotate(
    f"{num_other_projects} projects",  # Annotation text
    xy=(other_bar_value, other_index),  # Arrow tip (where it points)
    xytext=(other_bar_value + max(top_projects_df.sum()) * 0.05, other_index),  # Offset text to the right
    arrowprops=dict(arrowstyle="->", color="black", lw=1.5),  # Arrow properties
    fontsize=16,
    color="black",
    va="center"
)

# plot formatting
ax.set_xlabel('Node Hours', fontsize=16, labelpad=15)
ax.tick_params(axis='both', labelsize=14)

plt.legend(fontsize=16, loc='center right')
plt.tight_layout()
plt.show()
