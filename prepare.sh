#!/bin/bash

# Check for the correct number of arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <bagfile_folder> <output_folder>. Has to be absolute paths."
    exit 1
fi

# Assign input arguments to variables
bagfile_folder="$1"
output_folder="$2"

# Ensure the output directory exists
mkdir -p "$output_folder"

# Loop through all bag files in the bagfile folder
for bagfile in "$bagfile_folder"/*.bag; do
  # Extract the filename without the extension
  bagfile_name=$(basename "$bagfile" .bag)
  
  # Create a directory for this bag file in the output folder
  mkdir -p "$output_folder/$bagfile_name"
  
  # Convert the bag file to CSV
  python3 rosbag2csv/rosbag2csv.py "$bagfile" 2 ./topics.json -o "$output_folder/$bagfile_name/"
  mv "$output_folder/$bagfile_name/left--image_rect_color--compressed" "$output_folder/$bagfile_name/left_cam"
  mv "$output_folder/$bagfile_name/right--image_rect_color--compressed" "$output_folder/$bagfile_name/right_cam"
  
  # Generate heuristic labels for the left images
  python3 rowfollow_eval/get_heuristic_labels.py "$output_folder/$bagfile_name/left_cam" l -p rowfollow_eval/trained_parameters.ckpt
  
  # Generate heuristic labels for the right images
  python3 rowfollow_eval/get_heuristic_labels.py "$output_folder/$bagfile_name/right_cam" r -p rowfollow_eval/trained_parameters.ckpt
done

# example usage:
# source script.sh <bagfiles_input_directory> <output_directory> 
# -> not sure if the directories could be supplied as relative paths as well...
# source script.sh /home/tomwoe/Documents/ /home/tomwoe/Documents/dataset_creation/output