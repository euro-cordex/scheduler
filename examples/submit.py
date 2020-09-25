import os

from hpc_scheduler.scheduler import Scheduler
from configobj import ConfigObj

import logging


def add_job(sc, jobname, logdir, jobdir, header_dict, commands):
    # the fill dictionary is the input for the jobscrip template
    fill             = header_dict
    fill['log_dir']  = logdir
    fill['job_name'] = jobname

    # the name of the jobscript file
    jobscript = os.path.join(jobdir,jobname+'.sh') 
    # create a new job
    sc.create_job(jobname=jobname,jobscript=jobscript,
                  commands=commands,header_dict=fill,
                  write=True)


# define scheduler properties
SYS                 = 'SLURM'
pwd                 = os.getcwd()
logDir              = os.path.join(pwd,'logs')
jobDir              = os.path.join(pwd,'jobs')
# this is the file that will hold jobids of jobnames
schLogFile          = os.path.join(pwd,'my_scheduler.jobids.ini')
# the config file for the scheduler
schCfgFile          = os.path.join(pwd,'scheduler.ini')
schCfg              = ConfigObj(schCfgFile)
# the job script template
jobTpl              = schCfg['scheduler']['serial_template']
# a dictionary that contains input for the template
header_dict_default = schCfg['header']


# create a scheduler object, the scheduler will hold a number of jobs
scheduler  = Scheduler(SYS, name='my_scheduler', tpl=jobTpl, logfile=schLogFile)


# example application
# first, we create 10 jobs
nJobs      = 10
for i in range(1,nJobs+1):
    logging.info('creating job nr. {}'.format(i))
    jobname = 'my_job_nr{:03d}'.format(i)
    commands = "echo My job script nr. {}".format(i)
    add_job(scheduler, jobname, logDir, jobDir, header_dict_default, commands)

# now we can submit all jobs
scheduler.submit()
