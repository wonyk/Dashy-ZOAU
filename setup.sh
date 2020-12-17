#!/bin/bash

echo "Checking required files"
file="requirements.txt"
# Check if requirements.txt exists
if [[ -e "$file" ]] && [[ -s "$file" ]]; then
  echo "Downloading pip modules"
  pip3 install -r "$file"

  # Add banner to whatever is the choice of the user
  echo "Add start-up banner? [y/N]"
  read addBool
  echo "You have selected $addBool"

  if [[ "$addBool" =~ ^y(es)?$ ]]; then
    echo "Add to Z/OS Shell (z) or bash (b)?"
    read -n 1 shell
    # current_path=$(readlink -f "$0")
    script_dir=$(dirname "$BASH_SOURCE")
    current_dir=$(pwd)
    if [ $script_dir = '.' ]
    then
    script_dir="$current_dir"
    fi
    echo $script_dir
    # current_dir=$(dirname "$current_path")

    if [[ "$shell" == z ]]; then
      echo "Adding banner to Z/OS shell"
      echo "$script_dir/start.py" >> ~/.profile

    elif [[ "$shell" == b ]]; then
      echo "Adding banner to bash and default bash when login"
      echo "bash" >> ~/.profile
      echo "$script_dir/start.py" >> ~/.bashrc
    fi
  fi

  echo "Set up is complete."
  echo "Find out more about jobStat using jobStat.py --help"
else
  echo "Stopping... Some files are missing."
fi