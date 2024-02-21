#!/bin/bash

# Function to count the number of files recursively in a directory
count_files() {
    local dir="$1"
    local count=$(find "$dir" -type f | wc -l)
    echo "$count"
}

# Check for the correct number of arguments
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <input_directory>. Has to be an absolute path."
    exit 1
fi

# Assign input argument to a variable
input_directory="$1"
num_before=$(count_files "$input_directory")

# Loop through all files in the input directory
for dir in "$input_directory"/*; do
    if [ -d "$dir" ]; then
        # Run your Python3 module on the file
        python3 cleanup.py "$dir/left_cam"
        python3 cleanup.py "$dir/right_cam"
        # maybe also delete rosbag.csv ?
    fi
done

info_file="$input_directory/cleanup_info.txt"

# Check if info.txt exists, if not create it
if [ ! -e "$info_file" ]; then
    num_after=$(count_files "$input_directory")
    current_date=$(date +"%Y-%m-%d %H:%M:%S")
    echo -e "Number of files before cleanup(includes /heuristic contents): $num_before 
Number of files after cleanup: $num_after
    \nHeuristic accuracy of 100% would equal: Number of files after = Number of files before - Number of files after.
Actual Heuristic accuracy approximation: $num_after / ($num_before - $num_after): 
    \nApproximated accuracy of heuristic: $(echo "$num_after / ($num_before - $num_after)" | bc -l)
    \nDate of cleanup: $current_date" > "$info_file"
    echo "Info file created."
else
    echo "Info file already exists."
fi

