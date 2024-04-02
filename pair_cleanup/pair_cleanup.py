import argparse
import csv
import os
import shutil
import sys
import tempfile

def check_heudir_exists(dir_path):
    if not os.path.exists(dir_path):
        print('No heuristic_dir found at:', os.path.abspath(dir_path))
        print('Abort cleanup...')
        sys.exit(1)


def format_to_n_decimal_points(x, decimal_points):
    """ 
    Expects x to be either a list or of shape yyyymmdd-hhmmss-decimal_points_of_second_w_lines.png or 1START.png
    """
    if isinstance(x, list):
        for i in range(len(x)):
            x[i] = format_to_n_decimal_points(x[i], decimal_points)
        return x
    elif x == '1START.png':
        return x
    else:
        return x[:16+decimal_points]


def cleanup_dir(primary_dir, primary_heu_dir, secondary_heu_dir, primary_labels_file):
    """
    primary_dir is the one that is cleaned up. 
    secondary_dir is the one that is checked against.
    """
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='')

    with open(primary_labels_file, 'r', newline='') as infile, temp_file:
        reader = csv.reader(infile)
        writer = csv.writer(temp_file)

        # Write header if present
        header = next(reader)
        writer.writerow(header)

        matching_decimal_points = 0

        all_secondary_heu_images = format_to_n_decimal_points(os.listdir(secondary_heu_dir), matching_decimal_points)

        # Iterate through each row and copy if the condition is not met
        for row in reader:
            # assumes that image_name is first column always
            image_name = row[0]
            image_heu_name = image_name[:-4] + '_w_lines.png'
            # if the primary file exists then keep the label
            if os.path.exists(os.path.join(
                primary_heu_dir, image_heu_name)):
                writer.writerow(row)
                continue

            # check whether to delete the file 
            if not format_to_n_decimal_points(image_heu_name, matching_decimal_points) in all_secondary_heu_images:
                try: 
                    os.remove(os.path.join(primary_dir, image_name))
                except FileNotFoundError as e:
                    print(f'Tried to remove {os.path.join(primary_dir, image_name)}, but couldnt find it')


    # Replace the original file with the temporary file
    shutil.move(temp_file.name, primary_labels_file)
    print('Updated:', os.path.abspath(primary_labels_file))


def main():
    parser = argparse.ArgumentParser(
        prog='python3 cleanup.py', description='Cleans up the folders and labels.csv after manually deleting bad picks. Expects pair of directories')
    parser.add_argument(
        'input_dir1', help='First of the directories to be cleaned up. Expects this directory to have subdirectory /heuristic and a labels.csv present')
    parser.add_argument(
        'input_dir2', help='Second of the directories to be cleaned up. Expects this directory to have subdirectory /heuristic and a labels.csv present')

    args = parser.parse_args()

    input_dir1 = args.input_dir1
    input_dir2 = args.input_dir2
    print('##########################')
    print('Cleaning up:', os.path.abspath(input_dir1), 'and', os.path.abspath(input_dir2))
    labels_file1 = os.path.join(input_dir1, 'labels.csv')
    heuristic_dir1 = os.path.join(input_dir1, 'heuristic')
    labels_file2 = os.path.join(input_dir2, 'labels.csv')
    heuristic_dir2 = os.path.join(input_dir2, 'heuristic')
    check_heudir_exists(heuristic_dir1)
    check_heudir_exists(heuristic_dir2)

    cleanup_dir(input_dir1, heuristic_dir1, heuristic_dir2, labels_file1)
    cleanup_dir(input_dir2, heuristic_dir2, heuristic_dir1, labels_file2)

    shutil.rmtree(heuristic_dir1)
    print('Removed:', os.path.abspath(heuristic_dir1))
    shutil.rmtree(heuristic_dir2)
    print('Removed:', os.path.abspath(heuristic_dir2))


if __name__ == '__main__':
    main()
