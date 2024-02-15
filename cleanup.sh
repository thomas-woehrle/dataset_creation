#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_directory>. Has to be an absolute path."
    exit 1
fi

# Assign input argument to a variable
input_directory="$1"

# Loop through all files in the input directory
for dir in "$input_directory"/*; do
    # Check if the file is a regular file (not a directory)
    if [ -d "$dir" ]; then
        # Run your Python3 module on the file
        python3 cleanup.py "$dir/left_cam"
        python3 cleanup.py "$dir/right_cam"
        # maybe also delete rosbag.csv ?
    fi
done
