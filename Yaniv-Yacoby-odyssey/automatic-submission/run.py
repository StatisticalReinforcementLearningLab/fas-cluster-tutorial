import json
import os
import sys

# If this flag is set to True, the jobs won't be submitted to odyssey;
# they will instead be ran one after another in your current terminal
# session. You can use this to either run a sequence of jobs locally
# on your machine, or to run a sequence of jobs one after another
# in an interactive shell on odyssey.
DRYRUN = True

# This is the base directory where the results will be stored.
# On Odyssey, you may not want this to be your home directory
# If you're storing lots of files (or storing a lot of data).
OUTPUT_DIR = 'output'

# This list contains the jobs and hyper-parameters to search over.
# The list consists of tuples, in which the first element is
# the name of the job (here it describes the method we are using)
# and the second is a dictionary of parameters that will be
# be grid-searched over. That is, for the first item in the QUEUE below,
# the following jobs will be ran:
# 1. dataset='mnist', learning_rate=0.01
# 2. dataset='uci', learning_rate=0.001
# 3. dataset='mnist', learning_rate=0.001
# 4. dataset='uci', learning_rate=0.01
# Note that the second parameter must be a dictionary in which each
# value is a list of options.
QUEUE = [
    ('neural_network', dict(dataset=['mnist', 'uci'], learning_rate=[0.01, 0.001])),
    ('gaussian_process', dict(dataset=['mnist', 'uci'], optimize_lenscale=[True, False])),
]


def run(exp_dir, exp_name, exp_kwargs):
    '''
    This is the function that will actually execute the job.
    To use it, here's what you need to do:
    1. Create directory 'exp_dir' as a function of 'exp_kwarg'.
       This is so that each set of experiment+hyperparameters get their own directory.
    2. Get your experiment's parameters from 'exp_kwargs'
    3. Run your experiment
    4. Store the results however you see fit in 'exp_dir'
    '''
    print('Running experiment {}:'.format(exp_name))
    print('Results are stored in:', exp_dir)
    print('with hyperparameters', exp_kwargs)
    print('\n')


def main():
    assert(len(sys.argv) > 2)

    exp_dir = sys.argv[1]
    exp_name = sys.argv[2]
    exp_kwargs = json.loads(sys.argv[3])
    
    run(exp_dir, exp_name, exp_kwargs)


if __name__ == '__main__':
    main()
    
