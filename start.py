#!/usr/bin/env python3

#Import the Z Open Automation Utilities libraries as well as other libraries
from zoautil_py import MVSCmd, Datasets, Jobs
from zoautil_py.types import DDStatement
# from datetime import datetime
from termcolor import colored, cprint
import fire
import subprocess
# import time

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


# print('Breakdown:')
cprint('{:<8}'.format('ABEND') + '{:|<{num}}'.format('', num=round((systemAbend + userAbend) / jobCount * 100)), 'red')
cprint('{:<8}'.format('CC') + '{:|<{num}}'.format('', num=round(conditionCode / jobCount * 100)), 'yellow')
cprint('{:<8}'.format('Others') + '{:|<{num}}'.format('', num=round(others / jobCount * 100)), 'blue')
cprint('{:<8}'.format('Perfect') + '{:|<{num}}'.format('', num=round(goodCount / jobCount * 100)), 'green')

print(subprocess.check_output(['whoami']))
# colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
# count = 0
# table_header = ['Sys Abend', 'User Abend', 'CC Err', 'Others', 'Good!', 'Total', 'Percentage']
# percentage = round(goodCount / jobCount * 100, 2)
# table_data = [systemAbend, userAbend, conditionCode, others, goodCount, jobCount, percentage]
# dividers_len = 15 * len(table_header) + len(table_header) + 1
# divider_format = "{:-^{num}}"
# print(divider_format.format('', num = dividers_len))

# row_format ="{:^15}"
# print('|', end='')
# for header in table_header:
#   cprint(row_format.format(header), colors[count % 6], end='')
#   cprint('|', colors[count % 6], end='')
#   count += 1

# print('\n' + divider_format.format('', num = dividers_len))
# print('|', end='')

# for data in table_data:
#   cprint(row_format.format(data), colors[count % 6], end='')
#   cprint('|', colors[count % 6], end='')
#   count += 1
# print('\n' + divider_format.format('', num = dividers_len))








# table = Texttable()
# table.set_deco(Texttable.VLINES | Texttable.HEADER)
# table_header = ['Sys Abend', 'User Abend', 'CC Err', 'Others', 'Good!', 'Total', 'Percentage']
# table.set_cols_align(['c', 'c', 'c', 'c', 'c', 'c', 'c'])
# table.set_cols_valign(['t', 't', 't', 't', 't', 't', 't'])
# table.add_rows([table_header])

# cprint(table.draw(), 'blue')
# table.reset()
# table.set_deco(Texttable.VLINES)
# table.add_row([systemAbend, userAbend, conditionCode, others, goodCount, jobCount, goodCount / jobCount * 100])
# cprint(table.draw(), 'red')

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
