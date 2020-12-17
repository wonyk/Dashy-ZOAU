#!/usr/bin/env python3

# This python script is a simple tool to create a aesthetically pleasing information
# banner when users login. It utilises colors to make the terminal look more pleasing
# when logging into the USS. It pulls Job data using the ZOAU library. (Using jobStat.py)
# To fine tune job settings and color choices, please proceed to settings.py

#Import other libraries
from datetime import datetime
from termcolor import cprint
from jobStat import export_cli
import settings
import subprocess

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
name = settings.name if settings.name != '' else str(subprocess.check_output(['whoami']))[2:-3]

# The following is used for printing:
# Print banner
cprint("""
     ______    ______   _____ 
    |___  /   / / __ \ / ____|
       / /   / / |  | | (___  
      / /   / /| |  | |\___ \ 
     / /__ / / | |__| |____) |
    /_____/_/   \____/|_____/ 

""", settings.OSColor, attrs=['bold'])

# Set up the dict for basic system info and print them
detailsDict = {
  'Uptime': '{} {} hrs {} mins'.format(uptime_days, uptime_hours, uptime_mins), 
  'Load': load, 
  'User logins': user_count,
  # dd/mm/YY H:M:S
  'Date & Time': now.strftime("%d/%m/%Y %H:%M:%S")
}

for detail in detailsDict.items():
  cprint('{:.<15}: '.format(detail[0]), settings.detailsTitleColor, end='')
  cprint(detail[1], settings.detailsContentColor)
# Add newline
print('')

# Print the information by calling the jobStat CLI
export_cli(settings.job_scope, (), None, None, True)

# Cowsay, as usual. A tradition.
cprint("""
_______________ 
 Welcome back, 
 {:^13}
---------------
       \   ,__,
        \  (oo)____
           (__)    )\\
            ||--|| *
""".format(name), settings.cowsayColor)
