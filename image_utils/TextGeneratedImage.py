from os import popen
from pathlib import Path

class TextGeneratedImage:

  def __init__(self, path, im_params):
    self.path = path
    self.params = im_params if im_params else self.get_default_params()
    self.app = 'convert'
    self.front = 'images'


  def get_default_params(self):
    # dont put command line parameters in a plain string lol its not secure
    # ANYWAY heres some command line parameters.
    return '-background transparent -size 32x32 -fill white -pointsize 10 -gravity center -bordercolor gray50 -border 1x1'


  def get_path(self):
    return Path(self.front, self.path)


  def get_command_string(self):
    return "{} {} {}".format(self.app, self.params, str(self.get_path()))


  def generate_image(self):
    stream = popen(self.get_command_string())
    stream.read()


  def __repr__(self):
    return str(self.get_path())