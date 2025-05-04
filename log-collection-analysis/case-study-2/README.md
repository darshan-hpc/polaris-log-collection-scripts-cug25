**find-interesting-jobs-stdio.py**

This script analyzes aggregate STDIO job data to find interesting jobs to analyze. In particular, it prints out the 10 highest intensity jobs (in terms of total bytes).

`Usage: python find-interesting-jobs-stdio.py <job_stats_dir>`

The job in Case Study 2, 1977553-17460120447186390966.darshan, was selected for being the highest intensity job identified by this script.

The log file is included here for convenience. A PyDarshan job summary report can be generated to reproduce I/O cost and I/O operation count figures, Figure 7 and Figure 8, respectively.

`python -m darshan summary 1977553-17460120447186390966.darshan`
