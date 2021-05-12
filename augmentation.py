from Augmentor import Pipeline
import os
from shutil import move, copy, rmtree
import argparse
from matplotlib import pyplot as plt
import cv2 as cv
from PIL import Image

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
parser.add_argument('--test', '-t', help="Show an example", action='store_true')
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

    if args[-1] == True:
        method = f'{method}_test'
        print (method)

    save_folder = copy_files(os.path.join(source_folder, 'output'), method)
    rename_files(save_folder, method)


def get_original_image (file):
    temp = file.split('.')
    file = temp[0]
    file_extension = temp[1]

    file = file.split('_')
    return f'{file[-1]}.{file_extension}', f'{file[0]}'


def read_image (image_path):
    image = cv.imread(image_path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    return image


def plot_example (directory, method):
    directory = directory.replace ('/', '')

    folder_name = f'{directory}_{method}_test'
    file = os.listdir(folder_name)[0]
    original_file, original_folder = get_original_image(file)

    image = read_image(f'{folder_name}/{file}')
    original_image = read_image(f'{original_folder}/{original_file}')
    rmtree(folder_name)

    fig = plt.figure(figsize=(8, 8))
    fig.add_subplot (2, 1, 1).set_title ('result')
    plt.imshow(image)
    fig.add_subplot (2, 1, 2).set_title ('original image')
    plt.imshow (original_image)
    plt.show()


def augmentation_test (source_folder, method, sample, *args):
    augmentation(source_folder, method, sample, *args)
    plot_example(source_folder, method)


def main():
    if not args.test:
        augmentation(args.directory, args.method, args.sample, args.probability, args.first, args.second)
    else:
        augmentation_test (args.directory, args.method, 1, 1, args.first, args.second, True)


if __name__ == "__main__":
    main()
