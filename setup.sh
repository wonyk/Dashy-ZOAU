#!/bin/bash

# This script performs the basic set-up to ensure everything runs well and good
# Ensure you have ZOAU installed in USS: https://www.ibm.com/support/knowledgecenter/en/SSKFYE_1.0.1/install.html
# In case this script does not run well, you may perform the set-up manually by first installing the required pip3
# modules in requirements.txt. Next, you can manually add start.py to your .profile or .bashrc.

echo "Checking required files"
file="requirements.txt"
script_dir="$( cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 ; pwd -P )"

# Check if requirements.txt exists
if [[ -e "$script_dir/$file" ]] && [[ -s "$script_dir/$file" ]]; then
  echo "Downloading pip modules"
  pip3 install -r "$script_dir/$file"

  # Make sure they are executable
  chmod +x "$script_dir/start.py" "$script_dir/jobStat.py"

  # Add banner to whatever is the choice of the user
  echo "Add start-up banner? [y/N]"
  read addBool
  echo "You have selected $addBool"

  if [[ "$addBool" =~ ^y(es)?$ ]]; then
    echo "Add to Z/OS Shell (z) or bash (b)?"
    read shell

    # Loop until input is z or b
    while [[ "$shell" != z && "$shell" != b ]]; do
      echo "Invalid option. Add to Z/OS Shell (z) or bash (b)?"
      read shell
    done
  
    if [[ "$shell" == z ]]; then
      echo "Adding banner to Z/OS shell"
      echo "$script_dir/start.py" >> ~/.profile

    elif [[ "$shell" == b ]]; then
      echo "Adding banner to bash and default bash when login"
      echo "bash" >> ~/.profile
      echo "$script_dir/start.py" >> ~/.bashrc
    fi
    printf "Customise your start-up banner in settings.py\n"
  fi

  printf "Set up is complete.\n\n"
  echo "Find out more about jobStat using jobStat.py --help"
else
  echo "Stopping... Some files are missing."
fi