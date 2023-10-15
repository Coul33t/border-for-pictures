import os
import pathlib
from typing import List
import shutil

from PIL import Image as PilImage

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.image import Image as KivyImage

from plyer import filechooser # File Chooser


class WhiteBorder(Widget):

    white_border_size = ObjectProperty(None)
    top_bottom_black_size = ObjectProperty(None)
    left_right_black_size = ObjectProperty(None)
    image: ObjectProperty(None)

    def __init__(self):
        super(WhiteBorder, self).__init__()

        self.selection = None

        self.path_to_image = None
        self.image_name = None
        self.suffix = None
        self.tmp_path = None

        self.white_border_size_stored = 0
        self.black_v_border_size_stored = 0

    def load(self):
        print("Loading image")
        filechooser.open_file(on_selection=self.handle_selection)

    def handle_selection(self, selection):
        self.selection = selection
        if not self.selection:
            return

        if isinstance(selection, List):
            self.selection = selection[0]

        self.path_to_image = pathlib.Path(self.selection)
        self.image.source = self.path_to_image.as_posix()
        self.image_name = self.path_to_image.name[:-len(self.path_to_image.suffix)]
        self.suffix = self.path_to_image.suffix

    def preview(self):
        print(f"White border size: {self.white_border_size.text}")
        print(f"Vertical black border size: {self.top_bottom_black_size.text}")
        print(f"Horizontal black border size: {self.left_right_black_size.text}")

        self.white_border_size_stored = 0
        self.black_v_border_size_stored = 0

        if self.white_border_size.text:
            white_border_int = int(self.white_border_size.text)

            if white_border_int >= 0:
                self.white_border_size_stored = white_border_int
                im = PilImage.open(self.path_to_image)
                original_size = im.size
                new_size = (original_size[0] + white_border_int, original_size[1] + white_border_int)
                new_im = PilImage.new("RGB", new_size, (255, 255, 255))
                new_pos = (int(white_border_int / 2), int(white_border_int / 2))
                new_im.paste(im, new_pos)

                if self.top_bottom_black_size.text:
                    black_border_v_int = int(self.top_bottom_black_size.text)

                    if black_border_v_int > 0:
                        self.black_v_border_size_stored = black_border_v_int
                        new_size_black = (new_size[0], new_size[1] + black_border_v_int)
                        new_im_with_black = PilImage.new("RGB", new_size_black)
                        new_pos = (0, int(black_border_v_int / 2))
                        new_im_with_black.paste(new_im, new_pos)
                        new_im = new_im_with_black

                self.tmp_path = pathlib.Path(os.path.dirname(os.path.realpath(__file__)) + "/tmp/" + (self.image_name + "_tmp" + self.suffix))

                new_im.save(self.tmp_path)
        
                self.image.source = self.tmp_path.as_posix()
        
        self.image.reload()
                
                

    def save(self):
        print("Saving image")

        new_name = self.image_name
        if self.white_border_size_stored > 0:
            new_name += f"_wborder_{self.white_border_size_stored}"

        if self.black_v_border_size_stored > 0:
            new_name += f"_bborder_{self.black_v_border_size_stored}"

        breakpoint()
        shutil.move(self.tmp_path.as_posix(), (os.sep.join(self.tmp_path.parts[:-2]))[1:] + os.sep + "output" + os.sep + new_name)



class WhiteBorderApp(App):
    def build(self):
        return WhiteBorder()


if __name__ == '__main__':
    WhiteBorderApp().run()