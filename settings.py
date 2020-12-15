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

tableColor = [systemAbendColor, userAbendColor, conditionCodeColor, othersErrColor, goodJobsColor, totalCountColor, percentageColor]

cowsayColor = 'cyan'

# Jobs configurations
# Options:
# '*' - All jobs from every user on the system
# ['Z07216', 'Z99999'] - jobs under Z07216 and Z99999 only
# Any other invalid settings default to '*'
job_scope = '*'