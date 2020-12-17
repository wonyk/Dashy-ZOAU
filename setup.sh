#!/bin/bash

# This script performs the basic set-up to ensure everything runs well and good
# Ensure you have ZOAU installed in USS: https://www.ibm.com/support/knowledgecenter/en/SSKFYE_1.0.1/install.html
# We hope

echo "Checking required files"
file="requirements.txt"
script_dir=$(dirname "$BASH_SOURCE")
current_dir=$(pwd)
if [ $script_dir = '.' ]; then
  script_dir="$current_dir"
fi
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
    read -n 1 shell


    if [[ "$shell" == z ]]; then
      echo "Adding banner to Z/OS shell"
      echo "$script_dir/start.py" >> ~/.profile

    elif [[ "$shell" == b ]]; then
      echo "Adding banner to bash and default bash when login"
      echo "bash" >> ~/.profile
      echo "$script_dir/start.py" >> ~/.bashrc
    fi
  fi

  printf "Set up is complete.\n\n"
  printf "Customise your start-up banner in settings.py\n\n"
  echo "Find out more about jobStat using jobStat.py --help"
else
  echo "Stopping... Some files are missing."
fi