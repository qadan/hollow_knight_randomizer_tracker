from PIL import Image
from math import floor
from shutil import copy2
from os import popen, path

class ResourceIncludedImage:

  def __init__(self, path, im_params=None):
    self.path = path
    self.im_params = im_params if im_params else self.default_im_params()


  def get_padding_required(self, file):
    # Some of the images aren't perfectly square, so we want to know exactly
    # how much to jam on each side.
    image = Image.open(file)
    width, height = image.size
    # On abs 1 sides are 0.5 so no-op.
    if width == height or abs(width - height) == 1:
      return None
    elif height > width:
      splice = '{}x0'.format(floor((height - width) / 2))
      gravity = 'east'
    else:
      splice = '0x{}'.format(floor((width - height) / 2))
      gravity = 'south'
    return [
      {
        'background': 'transparent',
        'splice': splice
      },
      {
        'background': 'transparent',
        'gravity': gravity,
        'splice': splice,
      },
    ]


  def default_im_params(self):
    return {
      'background': 'transparent',
      'resize': '32x32',
      'gravity': 'center',
    }

  def convert_params(self, params):
    return ' '.join(['-{} {}'.format(param, value) for param, value in params.items()])


  def resize(self, destination, padding):
    for pad in padding:
      stream = popen('convert {} {}'.format(self.convert_params(pad), destination))
      out = stream.read()


  def copy_the_thing(self, destination):
    if path.isdir(destination):
      destination = '{}/{}'.format(destination, path.basename(self.path))
      print(destination)
    stream = popen('convert {} {} {}'.format(self.path, self.convert_params(self.im_params), destination))
    out = stream.read()
    padding = self.get_padding_required(destination)
    if padding:
      self.resize(destination, padding)


  def __repr__(self):
    return self.path


  def __str__(self):
    return self.path