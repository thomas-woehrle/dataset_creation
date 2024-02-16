import argparse
import csv
import os
import shutil
import tempfile


def main():
    parser = argparse.ArgumentParser(
        prog='python3 cleanup.py', description='Cleans up the folders and labels.csv after manually deleting bad picks')
    parser.add_argument(
        'input_dir', help='The input directory that needs to be cleaned up. Expects this directory to have subdirectory /heuristic and a labels.csv present')

    args = parser.parse_args()

    input_dir = args.input_dir
    print('##########################')
    print('Cleaning up:', os.path.abspath(input_dir))
    labels_file = os.path.join(input_dir, 'labels.csv')
    heuristic_dir = os.path.join(input_dir, 'heuristic')
    if not os.path.exists(heuristic_dir):
        print('No heuristic_dir found at:', os.path.abspath(heuristic_dir))
        print('Abort cleanup...')
        return

    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, newline='')

    with open(labels_file, 'r', newline='') as infile, temp_file:
        reader = csv.reader(infile)
        writer = csv.writer(temp_file)

        # Write header if present
        header = next(reader)
        writer.writerow(header)

        # Iterate through each row and copy if the condition is not met
        for row in reader:
            # assumes that image_name is first column always
            image_name = row[0]
            image_file = os.path.join(
                heuristic_dir, image_name[:-4] + '_w_lines.png')
            if not os.path.exists(image_file):
                os.remove(os.path.join(input_dir, image_name))
                continue
            writer.writerow(row)

    # Replace the original file with the temporary file
    shutil.move(temp_file.name, labels_file)
    print('Updated:', os.path.abspath(labels_file))
    shutil.rmtree(heuristic_dir)
    print('Removed:', os.path.abspath(heuristic_dir))


if __name__ == '__main__':
    main()
