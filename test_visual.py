import argparse
import cv2
import os
import pandas as pd
from rowfollow_eval.utils import get_filenames, process_image
from rowfollow_eval.keypoint_utils import Line, img_with_lines


def main():
    parser = argparse.ArgumentParser(
        prog='test_visual.py', description='Given an input directory, creates a new directory in there, where the pictures have the corresponding keypoints and lines on them.')

    parser.add_argument(
        'input_dir',  help='The input directory. Should have pictures and corresponding labels.csv inside.')
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = input_dir + '/test_visual'
    os.makedirs(output_dir, exist_ok=True)

    files = get_filenames(input_dir)
    files = sorted(files)

    df = pd.read_csv(input_dir + '/labels.csv')

    def to_tuple(str_tuple):
        tuple_elements = str_tuple.strip('()').split(',')
        tuple_integers = tuple(int(element.strip())
                               for element in tuple_elements)
        return tuple_integers

    for file in files:
        full_path = os.path.join(input_dir, file)
        np_array, image = process_image(full_path)
        csv_row = df[df['image_name'] == file]
        if csv_row.empty:
            continue
        csv_row = csv_row.iloc[0]
        vp = to_tuple(csv_row[1])
        ll = to_tuple(csv_row[2])
        lr = to_tuple(csv_row[3])

        lines = [Line(ll, vp, (0, 255, 0), 2), Line(lr, vp, (0, 0, 255), 2)]

        image = img_with_lines(image, lines)

        cv2.imwrite(os.path.join(output_dir, file[:-4] + '_test.png'), cv2.cvtColor(
            image, cv2.COLOR_RGB2BGR))


if __name__ == '__main__':
    main()
