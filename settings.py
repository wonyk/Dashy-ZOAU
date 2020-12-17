# This file contains the global settings. You may change the settings.
# Please provide correct inputs since the programme assume correct inputs.

# Colour Global settings
# Available choices: grey, red, green, yellow, blue, magenta, cyan, white
OSColor = 'blue'
detailsTitleColor = 'green'
detailsContentColor = 'cyan'
systemAbendColor = 'red'
userAbendColor = 'red'
conditionCodeColor = 'yellow'
othersErrColor = 'cyan'
goodJobsColor = 'green'
totalCountColor = 'white'
percentageColor = 'white'
tableBorderColor = 'white'
cowsayColor = 'cyan'

# Do not edit this list. Instead, edit the colors above for the respective components
tableColor = [systemAbendColor, userAbendColor, conditionCodeColor, othersErrColor, goodJobsColor, totalCountColor, percentageColor]

# Jobs configurations
# Options:
# 1. '*' - All jobs from every user on the system (wildcard)
# 2. ('Z07216', 'Z99999') - jobs under certain users only (Z07216 and Z99999 here)
# Any other invalid settings default to '*'
job_scope = '*'

# Name configuration.
# If left blank, it will default to your SSH user name.
# Please try to keep it under 13 characters
name = ''