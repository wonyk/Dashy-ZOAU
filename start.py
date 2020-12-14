#!/usr/bin/env python3

#Import the Z Open Automation Utilities libraries as well as other libraries
from zoautil_py import MVSCmd, Datasets, Jobs
from zoautil_py.types import DDStatement
from datetime import datetime
from termcolor import colored, cprint
from texttable import Texttable
import fire
import time

# Print banner
# print(r'''
#   ______    ______   _____ 
#  |___  /   / / __ \ / ____|
#     / /   / / |  | | (___  
#    / /   / /| |  | |\___ \ 
#   / /__ / / | |__| |____) |
#  /_____/_/   \____/|_____/ 
                           
# ''')

allJobs = Jobs.list(owner='*')
# allJobs = Jobs.list()
# Set up the variables
jobCount = len(allJobs)
goodCount = 0
userAbend = 0
systemAbend = 0
conditionCode = 0
others = 0

# Check for the various kind of errors to provide an overview
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

table = Texttable()
table.set_cols_align(['c', 'c', 'c', 'c', 'c', 'c', 'c'])
table.set_cols_valign(['t', 't', 't', 't', 't', 't', 't'])
table.add_rows([
  ['Sys Abend', 'User Abend', 'CC Err', 'Others', 'Good!', 'Total', 'Percentage'],
  [systemAbend, userAbend, conditionCode, others, goodCount, jobCount, goodCount / jobCount * 100]
  ])
print(table.draw())

# print('All jobs:', jobCount)
# print('CC0000:', goodCount)
# print('CC Others:', conditionCode)
# print('ABEND SXXX:', systemAbend)
# print('ABSEND UXXX:', userAbend)
# print('Others:', others)

# cprint('||||||||||||||||||', 'green')
# cprint('|||||||||||||||||||||||||||', 'red')
# starttime = time.time()
# lines = '|'
# while len(lines) < 6:
#     cprint('\r' + lines, 'blue', end='')
#     time.sleep(1.0 - (time.time() % 1.0))
#     lines += '|'

# print('')


# print(Datasets.hlq())

# print(Jobs.list(owner='*'))
