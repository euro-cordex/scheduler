
from hpc_scheduler.scheduler import Scheduler

# create a scheduler from a jobid logfile
scheduler = Scheduler('SLURM', logfile='my_scheduler.jobids.ini' )

# get a job accounting dictionary
accounting = scheduler.get_jobs_acct()
for jobname, acct in accounting.items():
    print(jobname, acct)

# make a lob of all jobs and status
scheduler.log_jobs_acct()

