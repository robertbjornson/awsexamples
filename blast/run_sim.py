#!/usr/bin/env python3

# run_sim.py <path to config.json>

import argparse
import logging
import json
import boto3
from pprint import pprint
import time
from math import pi as pi_real
import random

# Can't currently retrieve more than 100 jobs via DescribeJobs
CHUNKS_MAX=1000

# Job State headers
state_header = {
    'SUBMITTED':'SUB',
    'PENDING':'PEND',
    'RUNNABLE':'QUE',
    'STARTING':'STRT',
    'RUNNING':'RUN',
    'PI': 'PI ESTIMATE',
    'DELTA': 'DELTA'
}

progress_format = '{SUBMITTED:>4} {PENDING:>4} {RUNNABLE:>4} ' \
        '{STARTING:>4} {RUNNING:>4}'

def describe_all_jobs( batch_client, job_list ):
    # chunk job_list into sections (100 max per section, describe_job
    # limit)
    all_jobs = {'jobs':[]}
    for c in range(0, len(job_list), 100):
        response = batch_client.describe_jobs(jobs=job_list[c:c+100])
        all_jobs['jobs'] = all_jobs['jobs'] + response['jobs']
    return all_jobs


logging.basicConfig(level=logging.INFO)
# Set log level for boto components
logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)

valid_job_states = [
    'SUBMITTED', 'PENDING', 'RUNNABLE', 'STARTING', 'RUNNING',
    'SUCCEEDED', 'FAILED'
]

parser = argparse.ArgumentParser(
    description="Run PI simulation via AWS Batch"
)
parser.add_argument(
    '--job-name', dest='job_name',
    help='a name for this simulation',
    default='pi_sim'
)

args = parser.parse_args()

#   1. s3 bucket ready? create or empty as appropriate.
#   TODO: Actually do this...
#   1. do I have AWS credentials ready?
#   TODO: Actually do this...

# Job submission
#
# submit <chunks> jobs with parameters seed, iterations, and results_uri

job_list = []  # will contain list of job names submitted
client = boto3.client('batch')

seqs=101
chunk=30
jobs=list(enumerate([(i, min(i+chunk, seqs)) for i in range(0, seqs, chunk)]))

for jid, desc in jobs:
    # Creates a "folder" in s3 for this run's results
    results_uri = "/".join(['s3://myblast', args.job_name])
    # The individual job name is the root plus _<chunk number>
    job_name = "_".join([args.job_name, str(jid)])

    job_parameters = {
        'start': str(desc[0]),
        'end': str(desc[1]),
        'name': job_name,
        'results_uri': results_uri
    }

    response = client.submit_job(
        jobName = job_name,
        jobQueue = 'robq',
        jobDefinition = 'myblast:2',
        parameters = job_parameters
    )
    job_list.append( response['jobId'] )
    logging.debug('Submitted job ID: {}'.format(response['jobId']))

logging.info('Submitted jobs- monitoring progress')

# Monitor progress
#
# This process goes to monitor mode, displaying number of jobs in queue that
# are in the different states, e.g.:
#
# SUB | PEND | RUN |  F | S | ITER      | PI        | DELTA
#   0 |    3 |   2 |  0 | 5 | 500000    | 3.141583+ | 0.000012
#   0 |    0 |   3 |  0 | 7 | 700000    | 3.141545+ | 0.000005
#
# Complete: 10000000 iterations in 10 chunks yeilds pi: 3.1415965090909093

running = -1
s3r = boto3.resource('s3')
print( (progress_format).format(**state_header))

while True:
    # get job descriptions from job_list
    response = describe_all_jobs(client, job_list)
    summary = {}
    queue_stats = {
        'SUBMITTED':0,
        'PENDING':0,
        'RUNNABLE':0,
        'STARTING':0,
        'RUNNING':0,
        'PI':3,
        'DELTA':0
    }

    for state in valid_job_states:
        summary[state] = list(
            (j for j in response['jobs'] if( j['status'] == state))
        )
        queue_stats[state] = len(summary[state])

    running = len(
        summary['SUBMITTED'] + summary['PENDING'] +
        summary['RUNNABLE'] + summary['STARTING'] +
        summary['RUNNING']
    )

    if running == 0:
        print( "all jobs complete" )
        break
    else:
        # create running estimate of pi
        # get all created objects in result bucket if anything is done
        print((progress_format).format( **queue_stats)) 
        time.sleep(15)

# Complete



