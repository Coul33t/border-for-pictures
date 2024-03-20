import argparse

import pathlib
import os
from PIL import Image

def parserHandling():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", dest="input_path", help="Input folder to process", default="input/")
    parser.add_argument("-o", "--output", dest="output_path", help="Output folder to process", default="output/")
    parser.add_argument("-w", "--white_border_size", dest="white_border_size", help="White border size", default=50)
    return parser.parse_args()

def main(input_path, output_path, border_size = 50, add_black=False):
    im = Image.open(input_path)
    original_size = im.size
    new_size = (original_size[0] + border_size, original_size[1] + border_size)
    new_im = Image.new("RGB", new_size, (255, 255, 255))
    new_pos = (int(border_size / 2), int(border_size / 2))
    new_im.paste(im, new_pos)

    if add_black:
        new_size_black = (new_size[0], new_size[1] + 1000)
        new_im_with_black = Image.new("RGB", new_size_black)
        new_pos = (0, 500)
        new_im_with_black.paste(new_im, new_pos)
        new_im_with_black.save(pathlib.Path(output_path, input_path.stem + "_border_" + str(border_size) + "_black" + input_path.suffix))


    new_im.save(pathlib.Path(output_path, input_path.stem + "_border_" + str(border_size) + input_path.suffix))

if __name__ == "__main__":
    args = parserHandling()

    output_path = pathlib.Path(args.output_path)

    filenames = [path for path in os.listdir(args.input_path) if path[-3:] != "txt"]

    for file in filenames:
        file_input_path = pathlib.Path(args.input_path, file)
        main(file_input_path, args.output_path, args.white_border_size, False)