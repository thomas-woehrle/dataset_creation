# Dataset Creation Pipeline

Set of repositories to turn .bag files into labeled data with minimal human interaction.
The pipeline is specifically set up to work with the [terrasentia dataset of Jose Cuaran](https://github.com/jrcuaranv/terrasentia-dataset)

## Setup:

1. Have [dataset_creation repository](https://github.com/thomas-woehrle/dataset_creation) cloned (the repo, where this readme is inside).
2. Have the [rosbag2csv](https://github.com/thomas-woehrle/rosbag2csv) and [rowfollow_eval](https://github.com/thomas-woehrle/rowfollow_eval) repositories cloned and organized as subdirectories of this directory.
   So, the structure should be:
   /dataset_creation
   ... /rosbag2csv/
   ... /rowfollow_eval/
   Note that rowfollow_eval/ and rosbag2csv/ are in the .gitignore file of the dataset_creation repository
3. Have a `trained_parameters.ckpt` file at dataset_creation/rowfollow_eval/trained_parameters.ckpt

The only files in the subdirectories of this directory, which are directly called are rosbag2csv.py and get_heuristic_labels.py.
Some other files are used for util purposes, some files are not used at all, f.e. eval.py, heuristics_tryout.py, get_all_topics.py.

## Usage:

1. :
   `source prepare.sh /path/to/input_dir_with_bagfiles /path/to/output_dir`
   for example:
   `source prepare.sh /home/tom/Documents/research_assistance/ /home/tom/Documents/research_assistance/dataset`
   Should use absolute paths.

2. :
   Manually go through .../$bag_name/left_cam/heuristic and .../$bag_name/right_cam/heuristic and delete pics that have a bad heuristical prediction.

3. :
   `source cleanup.sh /path/to/output_dir`
   for example:
   `source cleanup.sh /home/tom/Dcouments/research_assistance/dataset`
   Should use absolute paths.

4. (completely optional):
   `python3 /path/to/file/test_visual.py $folder_name `
   f.e. `python3 ./cleanup.py ../../dataset/$bag_name/left_cam`
   -> will create new folder /test inside /left_cam and write pictures into it with labels as they are currently in /left_cam.csv,
   to check, if the labeling process makes sense

## Acknowledgements:

Written by [Thomas Woehrle](https://github.com/thomas-woehrle) in January and February of 2024. Supervised by [Arun Narenthiran V Sivakumar](https://github.com/ansivakumar).
See also acknowledgements in the README.md of the rosbag2csv and rowfollow_eval repositories.
