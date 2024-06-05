import argparse

import pathlib
import os
from PIL import Image

def parserHandling():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input_path", help="Input folder to process", default="input/")
    parser.add_argument("-o", "--output", dest="output_path", help="Output folder to process", default="output/")
    parser.add_argument("-w", "--white_border_size", dest="white_border_size", help="White border size", default=0, type=int)
    parser.add_argument("-s", "--make_square", dest="make_square", help="make the picture square by adding black border where needed", action='store_true')
    return parser.parse_args()

def compute_white_border_size(im_size):
    # Very arbitrary value
    return int((im_size[0] * im_size[1]) / 50000)

def processOnePicture(file_input_path, output_path, white_border_size, make_square):
    
    im = Image.open(file_input_path)
    original_size = im.size

    if white_border_size == 0:
        white_border_size = compute_white_border_size(original_size)


    new_size = (original_size[0] + white_border_size, original_size[1] + white_border_size)
    new_im = Image.new("RGB", new_size, (255, 255, 255))
    new_pos = (int(white_border_size / 2), int(white_border_size / 2))
    new_im.paste(im, new_pos)

    if make_square:
        # make new black image with old_smallest_edge = old_biggest_edge
        new_size_black = (max(new_size), max(new_size))
        new_im_with_black = Image.new("RGB", new_size_black)
        # center current picture in new image
        new_pos = (int((new_size_black[0] - new_size[0]) / 2), int((new_size_black[1] - new_size[1]) / 2))
        new_im_with_black.paste(new_im, new_pos)
        new_im_with_black.save(pathlib.Path(output_path, file_input_path.stem + "_border_" + str(white_border_size) + "_black" + file_input_path.suffix))


    new_im.save(pathlib.Path(output_path, file_input_path.stem + "_border_" + str(white_border_size) + file_input_path.suffix))

def main(args):
    output_path = pathlib.Path(args.output_path)

    filenames = [path for path in os.listdir(args.input_path) if path[-3:] != "txt"]

    for file in filenames:
        file_input_path = pathlib.Path(args.input_path, file)
        processOnePicture(file_input_path, output_path, args.white_border_size, args.make_square)

if __name__ == "__main__":
    args = parserHandling()
    main(args)