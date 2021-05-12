from Augmentor import Pipeline
import os
from shutil import move, copy, rmtree
import argparse

parser = argparse.ArgumentParser ()
parser.add_argument('directory', help="The source directory")
parser.add_argument('method', help="The method which you want to use",
                    choices=[
                        'rotate',
                        'zoom',
                        'flip_left_right',
                        'flip_top_bottom',
                        'zoom_random',
                        'crop_random'
                    ])
parser.add_argument('--probability', '-p', help="The probability", type=float, default=0.6)
parser.add_argument('--first', '-f',
                    type=float,
                    default=1.1,
                    help="zoom : min factor | rotate : max left rotation | zoom_random : percentage area | crop_random : percentage area")
parser.add_argument('--second', '-s',
                    type=float,
                    default=1.5,
                    help="zoom : max factor | rotate : max right rotation ")
parser.add_argument('--sample', '-S', help="Set sample by a number of images you want to augment, set sample = 0 to excute all images",
                    default=0, type=int)
args = parser.parse_args()


def check_existance (file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def copy_files (file_path, method):
    source_name = os.path.split (file_path)
    save_folder = f'{source_name[0]}_{method}'
    check_existance(save_folder)
    for file in os.listdir(file_path):
        source_path = os.path.join(file_path, file)
        copy (source_path, save_folder)

    rmtree(file_path)
    return save_folder


def rename_files (file_path, method):
    files = os.listdir(file_path)
    for file in files:
        name = file.split('.')
        new_file = name[0] + '.' + name[-1]
        new_file = new_file.replace('original', method)
        move(os.path.join(file_path, file), os.path.join(file_path, new_file))


def augment (source_folder, method, sample, *args):
    p = Pipeline(source_directory=source_folder)
    if method == "zoom":
        p.zoom(probability=args[0], min_factor=args[1], max_factor=args[2])
    elif method == "rotate":
        p.rotate(probability=args[0], max_left_rotation=args[1], max_right_rotation=args[2])
    elif method == "flip_left_right":
        p.flip_left_right(probability=args[0])
    elif method == "flip_top_bottom":
        p.flip_top_bottom(probability=args[0])
    elif method == "zoom_random":
        p.zoom_random(probability=args[0], percentage_area=args[1])
    elif method == "crop_random":
        p.crop_random(probability=args[0], percentage_area=args[1])

    if sample == 0:
        p.process()
    else:
        p.sample(sample)


def augmentation (source_folder, method, sample, *args):
    augment(source_folder, method, sample, *args)

    save_folder = copy_files(os.path.join(source_folder, 'output'), method)
    rename_files(save_folder, method)


def main():
    augmentation(args.directory, args.method, args.sample, args.probability, args.first, args.second)


if __name__ == "__main__":
    main()