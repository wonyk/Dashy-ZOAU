#!/usr/bin/env python3

# This python script is a simple tool to compile relevant job information using ZOAU
# You may view this as a "pro" version of the ZOAU Job function as it provides more details

#Import the Z Open Automation Utilities libraries as well as other libraries
from zoautil_py import Datasets, Jobs
from datetime import datetime
from termcolor import colored, cprint
import settings
import subprocess
import click

# Set up the variables
allJobs = []

# The CLI options are as follow:
# --users | -u : Filter jobs by user. Default is wildcard search. Else, provide multiple values
# --filter | -f : Filter jobs by error. Options: cc, sabend, uabend, others, good. Default to no filter. May select multiple values.
# --start : Start date to search for jobs. Format DD-MM-YYYY
# --end : End date to search for jobs. Format DD-MM-YYYY
# -p : Bool to print detailed output to STDOUT or file. Usually a SEQ Dataset
# --output | -o : Output file location and name. Will create the dataset if it does not exist and overwrite any existing files.

# Examples:
# ./job-stat.py : Returns all jobs stats in a table and bar chart form
# ./job-stat.py -u Z07216 -u Z09999 --start 15-12-2020 -p -o Z07216.OUTPUT(JOBCMPL) : Returns all jobs by users
# Z07216 and Z0999 on and after 15 Dec 2020 and output details to Z07216.OUTPUT(JOBCMPL)

@click.command()
@click.option('--users', '-u', multiple=True, default=['*'])
@click.option('--filter', '-f', multiple=True)
@click.option('--start', type=click.DateTime(formats=["%d-%m-%Y"]))
@click.option('--end', type=click.DateTime(formats=["%d-%m-%Y"]))
@click.option('-p', is_flag=True)
@click.option('-o', '--output')
def cli(users, filter, start, end, p, output):
  getJobs(users)
  # If there are error filters, filter the results accordingly
  if filter != None:
    filterJobs(filter)
  displayStats()

# Get all jobs based on user filter first. Date filter will be performed later.
def getJobs(filter):
  global allJobs
  if (type(filter) == tuple):
    if (len(filter) != 0):
      for user in filter:
        jobsList = Jobs.list(owner=user)
        if jobsList != None:
          allJobs.extend(jobsList)
  else:
    # Else, the wildcard will be used
    allJobs = Jobs.list(owner='*')

# Filter the jobs by error codes:
def filterJobs(filters):
  global allJobs
  tempList = []

  for f in filters:
    if f == 'uabend':
      tempList.extend(filter(userAbendFilter, allJobs))
    elif f == 'sabend':
      tempList.extend(filter(systemAbendFilter, allJobs))
    elif f == 'cc':
      # filtered = filter(ccErrFilter, allJobs)
      tempList.extend(filter(ccErrFilter, allJobs))
    elif f == 'others':
      tempList.extend(filter(othersFilter, allJobs))
    elif f == 'good':
      tempList.extend(filter(goodFilter, allJobs))
    else:
      print(f'Filter {f} not valid. Removing all filters.')
      return
  
  allJobs = tempList

# All the separate filters used:
def userAbendFilter(job):
  if (job['status'] == 'ABEND' and job['return'][:1] == 'U'):
    return True
  return False

def systemAbendFilter(job):
  if (job['status'] == 'ABEND' and job['return'][:1] == 'S'):
    return True
  return False

def ccErrFilter(job):
  if (job['status'] == 'CC' and job['return'] != '0000'):
    return True
  return False

def othersFilter(job):
  code = job['status']
  if (code != 'ABEND' and code != 'CC'):
    return True
  return False

def goodFilter(job):
  if (job['status'] == 'CC' and job['return'] == '0000'):
    return True
  return False


def displayStats():
  # declare global variables and local ones
  global allJobs
  goodCount = 0
  userAbend = 0
  systemAbend = 0
  conditionCode = 0
  others = 0

  # Check for the various kind of errors to provide an overview
  # Perform various calculations
  jobCount = len(allJobs)

  for job in allJobs:
    # Check Abend code
    if (job['status'] == 'ABEND'):
      if (job['return'][:1] == 'S'):
        systemAbend += 1
      elif (job['return'][:1] == 'U'):
        userAbend += 1
      else:
        others += 1
    # Check CC codes
    elif (job['status'] == 'CC'):
      if (job['return'] == '0000'):
        goodCount += 1
      else:
        conditionCode += 1
    else:
      others += 1

  # Get other system details
  now = datetime.now()

  # The following is used for printing:
  # Print banner
  cprint("""
             __      __         _____ __        __ 
            / /___  / /_       / ___// /_____ _/ /_
       __  / / __ \/ __ \______\__ \/ __/ __ `/ __/
      / /_/ / /_/ / /_/ /_____/__/ / /_/ /_/ / /_  
      \____/\____/_.___/     /____/\__/\__,_/\__/  

  """, settings.OSColor, attrs=['bold'])

  # Set up the table headers and borders first
  count = 0
  table_header = ['Sys Abend', 'User Abend', 'CC Err', 'Others', 'Good!', 'Total', 'Percentage']
  percentage = round(goodCount / jobCount * 100, 2)
  table_data = [systemAbend, userAbend, conditionCode, others, goodCount, jobCount, percentage]
  # Need to add the number of dividers
  dividers_len = 15 * len(table_header) + len(table_header) + 1

  # Print the top border
  divider_format = "{:-^{num}}"
  cprint(divider_format.format('', num = dividers_len), 'magenta')

  # Print the header itself
  colors = settings.tableColor
  row_format ="{:^15}"
  # Fenceposting...
  print('|', end='')
  for header in table_header:
    cprint(row_format.format(header), colors[count], end='')
    cprint('|', colors[count], end='')
    count += 1
  print('\n' + divider_format.format('', num = dividers_len))
  print('|', end='')

  # Print the data row, again using fencepost technique
  count = 0
  for data in table_data:
    cprint(row_format.format(data), colors[count], end='')
    cprint('|', colors[count], end='')
    count += 1
  print('\n' + divider_format.format('', num = dividers_len), end='\n\n')

  # Print individual breakdown in a nice "bar" chart
  chartDict = {
    'ABEND': {
      'num': round((systemAbend + userAbend) / jobCount * 100),
      'color': settings.systemAbendColor
    },
    'CC': {
      'num': round(conditionCode / jobCount * 100),
      'color': settings.conditionCodeColor
    },
    'Others': {
      'num': round(others / jobCount * 100),
      'color': settings.othersErrColor}
      ,
    'Perfect': {
      'num': round(goodCount / jobCount * 100),
      'color': settings.goodJobsColor
    }
  }

  cprint('Breakdown:', 'white', attrs=['underline'])
  for category in chartDict:
    cprint('{:<8}'.format(category) + '{:|<{num}} {num}%'.format('', num=chartDict[category]['num']), chartDict[category]['color'])


if __name__ == '__main__':
  cli()