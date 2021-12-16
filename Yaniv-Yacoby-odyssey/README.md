# Odyssey Tools

This repository contains a collection of tools and helpful notes about using Odyssey.

Why should you use Odyssey? Reasons include...
* Need to run code for many hours, and it's too annoying to run it on your laptop
* Need to run a bunch of code in parallel (e.g. fit a model using 100 different hyper-parameters)
* Need access to GPUs

Since resources on Odyssey are shared, it's important to know how to use the resources respectfully. 

Helpful links:
* [Getting access](https://docs.rc.fas.harvard.edu/kb/how-do-i-get-a-research-computing-account/)
* [Documentation](https://docs.rc.fas.harvard.edu/)


## Logging in (via Terminal)

Here we provide instructions for how to log into Oddysey via terminal. 
See the documentation for more info, or for alternative methods of accessing Odyssey.

1. In your terminal: `ssh USERNAME@login.rc.fas.harvard.edu`.   
  * Odyssey will require a password, and then a verification code (2-factor authentication). 
  * Tip: instead of typing the verification code from the DuoMobile phone app, install the Java desktop app mentioned [here](https://docs.rc.fas.harvard.edu/kb/openauth/). You will then be able to copy directly the codes from the app into your terminal, which will save you a lot of time.
2. You are now logged into one of Odyssey's "login nodes". These nodes are **not** for running computation jobs; from these login nodes you will be able to spawn jobs to do your actual computation (see details below). This is your home directory. Here, you can clone your github repository, look around, and run terminal commands (so long as you don't do anything super expensive, like training a model). 
3. On odyssey, you cannot install software. Instead, you have to use their module library to load tools you need. For example, to load Python3.6, git, and CUDA (for using the GPUs), you will need to run the following commands: 
```
module load cuda/9.0-fasrc02 cudnn/7.0_cuda9.0-fasrc01
module load python/3.6.3-fasrc01
module load git
```
The full list of modules can be found [here](https://portal.rc.fas.harvard.edu/p3/build-reports/).
We recommend you put the modules you regularly rely on into your `.bashrc` file so that they are loaded every time you open the terminal. 
If you're not familiar with `.bashrc` files, you can read more about them [here](https://www.journaldev.com/41479/bashrc-file-in-linux). 

Once the models are loaded, you can install / load your python environment and install whichever packages you need. 

After completing these steps, you are ready to run more heavy-duty computation on Odyssey.

## Running Code on Odyssey

Broadly, Odyssey allows you to run two types of jobs: interactive shells, and batch jobs.
An "interactive shell" allows you to run your code and interact with it (e.g. you can see its output print on your screen, you can interrupt the execution using Control-C, etc.). On the other hand, a batch job is a job that you do not directly interact with -- you tell the job manager (called SLURM) what to execute, and where to store the print statements, and the job manager allocates a machine for you and runs it. In the batch job case, you can still kill your job, but only by interacting with the job manager. 

Typically, you would want to use an interactive job in the following cases:
* You only need to run a few things
* You want to interact with your job (e.g. use the debugger)

On the other hand, you would likely want a batch job when needing to run a bunch of things simultaneously. 
We'll describe below how to run each type of job. 


### Running an "Interactive Shell" Job

To run an interactive shell, simply use the command, `srun -p PARTITION --pty --mem MEMORY -t TIME bash`,
where PARTITION specifies from which group of machines you want your shell to run on,
MEMORY (in MB) specifies how much memory to give your shell, and TIME (in D-HH:MM) specifies how long until your job is automatically killed. 
For example, you can run `srun -p test --pty --mem 5000 -t 0-02:00 bash`. 
To determine which partition best suits you, check out the "Slurm Partitions" section [here](https://docs.rc.fas.harvard.edu/kb/running-jobs/).

Once you've executed the above command, you'll be logged into a new node that you can run whatever you like on.
When you are done using the interactive shell, you can type `exit`.

**Note:** if you lose network connection or close your terminal, your interactive shell will immediately be killed (which is super inconvenient!).
To deal with this, we recommend you use `tmux` (described in the `tmux` directory of this repository).

### Using Jupyter Notebooks Remotely

You can also use interactive shell jobs to run Jupyter notebooks, which you can access through your web browser! See instructions [here](https://docs.rc.fas.harvard.edu/kb/jupyter-notebook-server-on-cluster/).


### Running Batch Jobs

To run a batch job, you first need to write a slurm script. This script will tell the slurm job manager how to run your job, and how much resources to allocate to your job. Here's an example slurm script:
```
#!/bin/bash
#SBATCH -n 1 # Number of cores
#SBATCH -N 1 # Ensure that all cores are on one machine
#SBATCH -t 0-10:00 # Runtime in D-HH:MM
#SBATCH -p serial_requeue # Partition to submit to
#SBATCH --mem=5000 # Memory pool for all cores (see also --mem-per-cpu)
#SBATCH -o OUTPUTDIR/out_%j.txt # File to which STDOUT will be written
#SBATCH -e OUTPUTDIR/err_%j.txt # File to which STDERR will be written

python your_code.py # how to run your job
```
Notice that it contains nearly the same info as the command required to spawn an interactive shell. 
To actually submit the job to the job manager, you will have to run `sbatch PATH-TO-SLURM-SCRIPT`. 
Once you have done that, the only way for you to check on your job's progress is by looking at the files to which you directed
your program's printing to (i.e. STDOUT and STDERR),
or via slurm commands (see the useful odyssey commands below). 

Now, if you wanted to submit many jobs, each for instance training a different model on a different data-set using different hyper-parameters,
you would need to programmatically generate these slurm scripts.
Since this is annoying to write, we've provided you with code to take care of the annoying bits.
The code and documentation can be found in the `automatic-submission` directory in this repository. 


### Some Useful Odyssey Commands

If you have a job running on Odyssey (as an interactive shell or as a batch job), here are some useful commands:
* Check on job status `sacct`
* Cancel all jobs you submitted: `scancel -u USERNAME`
* Cancel a specific job: `scancel JOBID`
* List all jobs on a specific partition: `showq-slurm -l -o -p PARTITION` (you can then `grep` for your username).
* Alias `LIST_JOBS` for listing jobs in a user-friendly manner: `alias LIST_JOBS='sacct -X --format=JobId,JobName%64,Partition,Start,Elapsed,Timelimit,State'`
* Alias `STOP_RUNNING` for cancelling all your running jobs: `alias STOP_RUNNING='sacct -X --format=JobId,State | grep RUNNING | cut -c -8 | xargs scancel'`
* Alias `STOP_PENDING` for cancelling all your pending jobs: `alias STOP_PENDING='sacct -X --format=JobId,State | grep PENDING | cut -c -8 | xargs scancel'`

# Additional Tips

1. Separate your code into **two parts:** (1) a script that trains models (on different datasets, with different parameters) and stores the resultant model to disk (e.g. using a pickle file), and (2) a script that reads the trained models from file, computes all evaluation metrics and produces all visualizations. This way, if you need to make a quick change to a metric or a visualization, you do not need to re-train your models. You can have the second script be automatically ran using the first script.
2. If your visualizations / metrics script takes a long time to run, consider parallelizing it on Odyssey as well. 
3. In each results file, store the commit version of your repository in case you ever need to figure out which version of the code something was computed with. You can do this in python like [this](https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script).
4. Once your visualization / metrics script computes the necessary info for every run of your model / data, you will likely need to do some **model selection**. For this, we recommend you load all metrics you computed for every model/data-set/hyper-parameters into a pandas dataframe, and then write your model selection code in terms of operations on that data-frame. Your code will be cleaner and easy to modify this way. Additionally, dataframes can be exported into [latex](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_latex.html) so that you can just plop them straight into your paper. 



