## Description
The `pair_cleanup.sh` script operates on the level of days. So, f.e. a input directory could be `20230609_tomato`. It expects that inside this input directory, there are sub directories, 
which correspond to bag files. It then expects inside these bag file subdirectories to be pairs of subdirectories. Specifically, `left_cam` and `right_cam` or `front_left_cam`, `front_right_cam`,
`rear_left_cam`, `rear_right_cam`. All other structures will be dismissed as "Invalid directory structure". 

`pair_cleanup.py` operates on the level of pairs of cams.

After running pair_cleanup.sh correctly, only pictures remain, if :
1. they have a good heuristical prediction. In this case, their label can be found in the labels.csv file of the cam
2. their counterpart, taken at the same time but at the other camera, has a good heuristical prediction. In this case, they don't have a label in the corresponding labels.csv file

## Usage

1. Manually go through /path/to/output_dir/$bag_name/<cam_name>/heuristic for each cam and each bag. Delete the pictures that have a bad heuristical prediction (-> do the lines match the row?). 
Keep the pictures that have a good heuristical prediction.

2. Cleanup the directories, leaving behind only pictures which have good predictions inside respective labels.csv
   <br>
   `source cleanup.sh /path/to/output_dir`
   <br>for example:
   `source cleanup.sh /home/tom/Dcouments/20230609_tomato`
   <br>Should use absolute paths.

5. (completely optional)
   <br>
   `python3 /path/to/file/test_visual.py $folder_name `
   <br>f.e. `python3 test_visul.py 20230609_tomato/<bag_name>/right_cam`
   -> will create new folder /test_visual inside /right_cam and write pictures into it with labels as they are currently in /right_cam/labels.csv,
   to check, if the labeling process makes sense
   <br> test_visual.py can be found in the parent directory of /pair_cleanup.

## Example of folder structure

  For example, the content of `20230609_tomato` could be:
```
/<bag_name>
    /left_cam
        picture1.png
        …
        pictureN.png
        /heuristic
            picture1_heuristic.png
            ….
            pictureN_heuristic.png
        labels.csv
    /right_cam
        same_structure_as_left_cam
/<other_bag_name>
    ...
```
