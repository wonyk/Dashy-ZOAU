#!/usr/bin/env python3

#Import the Z Open Automation Utilities libraries as well as other libraries
from zoautil_py import Datasets, Jobs
from datetime import datetime
from termcolor import colored, cprint
import subprocess

# Uncomment the following to list all jobs (default)
allJobs = Jobs.list(owner='*')

# Uncomment the following line to list jobs by you only.
# allJobs = Jobs.list()

# Set up the variables
goodCount = 0
userAbend = 0
systemAbend = 0
conditionCode = 0
others = 0
jobCount = len(allJobs)

# Check for the various kind of errors to provide an overview
# Perform various calculations
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

# Sample Format of raw_uptime:
#  8 day(s), 13:28,  11 users,  load average: 0.00, 0.00, 0.00
raw_uptime = str(subprocess.check_output(['uptime']))[13:-3]
arr = raw_uptime.split(', ')
uptime_days = arr[0][1:]
uptime_hours = arr[1].split(':')[0]
uptime_mins = arr[1].split(':')[1]
user_count = arr[2][1:-5]
load = raw_uptime.split(':')[2][1:]

# Get other system details
now = datetime.now()
name = str(subprocess.check_output(['whoami']))[2:-3]

# The following is used for printing:
# Print banner
cprint("""
     ______    ______   _____ 
    |___  /   / / __ \ / ____|
       / /   / / |  | | (___  
      / /   / /| |  | |\___ \ 
     / /__ / / | |__| |____) |
    /_____/_/   \____/|_____/ 

""", "blue", attrs=['bold'])

# Set up the dict for basic system info and print them
detailsDict = {
  'Uptime': '{} {} hrs {} mins'.format(uptime_days, uptime_hours, uptime_mins), 
  'Load': load, 
  'User logins': user_count,
  # dd/mm/YY H:M:S
  'Date & Time': now.strftime("%d/%m/%Y %H:%M:%S")
}

for detail in detailsDict.items():
  cprint('{:.<15}: '.format(detail[0]), 'green', end='')
  cprint(detail[1], 'cyan')
# Add newline
print('')

# Set up the table headers and borders first
colors = ['red', 'red', 'yellow', 'blue', 'green', 'white', 'white']
count = 0
table_header = ['Sys Abend', 'User Abend', 'CC Err', 'Others', 'Good!', 'Total', 'Percentage']
percentage = round(goodCount / jobCount * 100, 2)
table_data = [systemAbend, userAbend, conditionCode, others, goodCount, jobCount, percentage]
# Need to add the number of dividers
dividers_len = 15 * len(table_header) + len(table_header) + 1

# Print the top border
divider_format = "{:-^{num}}"
print(divider_format.format('', num = dividers_len))

# Print the header itself
row_format ="{:^15}"
# Fenceposting...
print('|', end='')
for header in table_header:
  cprint(row_format.format(header), colors[count], end='')
  cprint('|', colors[count % 6], end='')
  count += 1
print('\n' + divider_format.format('', num = dividers_len))
print('|', end='')

# Print the data row, again using fencepost technique
count = 0
for data in table_data:
  cprint(row_format.format(data), colors[count], end='')
  cprint('|', colors[count % 6], end='')
  count += 1
print('\n' + divider_format.format('', num = dividers_len), end='\n\n')

# Print individual breakdown in a nice "bar" chart
cprint('Breakdown:', 'white', attrs=['bold', 'underline'])
cprint('{:<8}'.format('ABEND') + '{:|<{num}}'.format('', num=round((systemAbend + userAbend) / jobCount * 100)), 'red')
cprint('{:<8}'.format('CC') + '{:|<{num}}'.format('', num=round(conditionCode / jobCount * 100)), 'yellow')
cprint('{:<8}'.format('Others') + '{:|<{num}}'.format('', num=round(others / jobCount * 100)), 'blue')
cprint('{:<8}'.format('Perfect') + '{:|<{num}}'.format('', num=round(goodCount / jobCount * 100)), 'green')

print("""
_______________ 
 Welcome back, 
 {:^13}
---------------
       \   ,__,
        \  (oo)____
           (__)    )\\
            ||--|| *
""".format(name))
