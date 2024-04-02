#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_directory>. Has to be an absolute path."
    exit 1
fi

# Assign input argument to a variable
input_directory="$1"

find "$input_directory" -mindepth 1 -maxdepth 1 -type d | while read -r dir; do
    # Check if the directory contains left_cam and right_cam subdirectories
    if [ -d "$dir/left_cam" ] && [ -d "$dir/right_cam" ]; then
        python3 pair_cleanup.py "$dir/left_cam" "$dir/right_cam"
    # check if alternatively, it contains front_left_cam and front_right_cam as well as rear cams
    elif [ -d "$dir/front_left_cam" ] && [ -d "$dir/front_right_cam" ] && [ -d "$dir/rear_left_cam" ] && [ -d "$dir/rear_right_cam" ]; then
        python3 pair_cleanup.py "$dir/front_left_cam" "$dir/front_right_cam"
        python3 pair_cleanup.py "$dir/rear_left_cam" "$dir/rear_right_cam"
    else
        echo "Invalid directory structure in $dir"
    fi
done
