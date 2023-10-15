import pathlib
import os
from PIL import Image

def load_image(input_path: str) -> Image:
   im = Image.open(input_path)
   return im 

def get_auto_border_size():
    pass

def add_white_borders(im: Image, auto_border_size = True, border_size = 50):
    original_size = im.size

    if (auto_border_size):
        border_size = get_auto_border_size()

    new_size = (original_size[0] + border_size, original_size[1] + border_size)
    # Create a new image (blank one)
    new_im = Image.new("RGB", new_size, (255, 255, 255))
    # Compute where the top left corner will be on the new image
    new_pos = (int(border_size / 2), int(border_size / 2))
    # Paste the original image in the middle of it
    new_im.paste(im, new_pos)

    return new_im, im.size

def add_black_borders(im: Image, original_size, auto_border_size = True, border_size = 50) -> Image:
    if (auto_border_size):
        border_size = get_auto_border_size()

    new_size = (original_size[0] + border_size, original_size[1] + border_size)
    new_size_black = (new_size[0], new_size[1] + 1000)
    new_im_with_black = Image.new("RGB", new_size_black)
    new_pos = (0, 500)
    new_im_with_black.paste(im, new_pos)
    return new_im_with_black

def process_picture(input_path, output_path, auto_border_size = True, border_size = 50, add_black=False):
    im = load_image(input_path)

    new_im, im_size = add_white_borders(im, auto_border_size, border_size)

    # If black borders must be added, do the same, but with a black image (size is fixed for now)
    if add_black:
        new_im_with_black = add_black_borders(new_im, im_size)
        new_im_with_black.save(pathlib.Path(output_path, input_path.stem + "_border_" + str(border_size) + "_black" + input_path.suffix))       

    # Save the image in the output folder
    new_im.save(pathlib.Path(output_path, input_path.stem + "_border_" + str(border_size) + input_path.suffix))

def main():
    # Input and output folders paths
    input_folder = "input/"
    output_folder = "output/"

    # Make it a pathlib Path because it's easier to use
    output_path = pathlib.Path(output_folder)

    # Get all the filenames in the input folder (except for the "keep.txt" file)
    filenames = [path for path in os.listdir(input_folder) if path[-3:] != "txt"]

    # White border size (in pixels)
    border_size = 25

    # For each file in the input folder
    for file in filenames:
        # Create a path (input_folder/file.jpg)
        input_path = pathlib.Path(input_folder, file)
        process_picture(input_path, output_path, border_size=border_size, add_black=False)

if __name__ == "__main__":
    main()