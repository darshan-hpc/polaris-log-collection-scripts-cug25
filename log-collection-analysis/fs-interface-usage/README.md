**extract-fs-interface-data.py**

This script calculates aggregate job statistics for each storage system using each interface. The results are stored in a CSV file (fs_interface_usage.csv) that is fed to other plotting scripts.

`Usage: python extract-fs-interface-data.py <job_stats_dir>`

`<job_stats_dir>` is the directory containing all the CSV files generated by the `extract-job-stats.py` script.

**plot-interface-bars-jobs.py**

This script plots a grouped bar chart of total jobs acessing each storage system using each interface.

`Usage: python plot-interface-bars-jobs.py <fs_interface_usage>`

`<fs_interface_usage>` is the path to the CSV generated by `extract-fs-interface-data.py`.

**plot-interface-bars-bytes.py**

This script plots a grouped bar chart of total bytes accessed on each storage system using each interface.

`Usage: python plot-interface-bars-bytes.py <fs_interface_usage>`

`<fs_interface_usage>` is the path to the CSV generated by `extract-fs-interface-data.py`.
