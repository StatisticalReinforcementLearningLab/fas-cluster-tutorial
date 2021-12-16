import os
import copy
import sys
import itertools
import json
import subprocess
import socket

from run import (
    run,
    QUEUE,
    DRYRUN,
    OUTPUT_DIR,
)


TMP_DIR = 'tmp'
TEMPLATE = 'template.sh'


def safe_zip(*args):
    if len(args) > 0:
        first = args[0]
        for a in args[1:]:
            assert(len(a) == len(first))

    return list(zip(*args))


def submit_job(output_dir, template, exp_name, exp_kwargs):
    exp_dir = os.path.join(output_dir, exp_name)
    if not os.path.exists(exp_dir):
        os.makedirs(exp_dir)

    script = copy.deepcopy(template)
    script = script.replace('EXPNAME', exp_name)
    script = script.replace('EXPDIR', exp_dir)
    script = script.replace('KWARGS', "'{}'".format(json.dumps(exp_kwargs)))
    
    sname = os.path.join(TMP_DIR, 'slurm_{}.sh'.format(exp_name))
    with open(sname, 'w') as f:
        f.write(script)
    
    if not DRYRUN:
        ret = subprocess.call('sbatch {}'.format(sname).split(' '))
        if ret != 0:
            print('Error code {} when submitting job for {}'.format(ret, sname))
    else:
        run(exp_dir, exp_name, exp_kwargs)
    

def main():
    # Create the directory where your results will go.
    # In this directory you can make a sub-directory for each experiment you run.
    # Experiments are listed in the 'QUEUE' variable above
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Create a temporary directory for the slurm scripts
    # that are automatically generated by this script
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    # Read in the template so we can modify it programmatically
    with open(TEMPLATE, 'r') as f:
        template = f.read()

    # For each experiment, create a job for every combination of parameters
    for experiment_name, params in QUEUE:
        for vals in itertools.product(*list(params.values())):
            exp_kwargs = dict(safe_zip(params.keys(), vals))
            submit_job(OUTPUT_DIR, template, experiment_name, exp_kwargs)


if __name__ == '__main__':
    main()


