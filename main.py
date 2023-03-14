import pathlib

from PIL import Image

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
    filename = "0009_7_retouchee_recadree.jpg"
    input_folder = "input"
    output_folder = "output"

    input_path = pathlib.Path(input_folder, filename)
    output_path = pathlib.Path(output_folder)
    border_size = 50

    main(input_path, output_path, border_size, True)