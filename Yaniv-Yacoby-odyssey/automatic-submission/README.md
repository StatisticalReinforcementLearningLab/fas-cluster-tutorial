# Automatic Submission Script

This script will help you automatically create a sequence of jobs by appropriately generating the SLURM scripts and submitting them.
To use this script, copy the files in this directory into your code-base.
There are two files you need to modify:
1. Modify the `template.sh` file so that your job is submitted to the right partition, given the right amount of memory, etc.
2. Modify `run.py` as instructed inside the file. 

To get a sense for what the script does, simply run it **as is** using `python submit_batch.py`. 






