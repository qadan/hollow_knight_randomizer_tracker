from os import popen
from yaml import safe_load
from image_utils.TextGeneratedImage import TextGeneratedImage

class GenerateSkips:

  def __init__(self, destination):
    self.skips = None
    self.destination = destination


  def load_skips(self):
    with open('resources/rules/skips.yaml', 'r') as skip_yaml:
      return safe_load(skip_yaml)


  def get_skip_text_img(self, option, label):
    params = '-size 128x32 -background transparent -pointsize 15 -gravity east -fill white label:\'{}\''.format(label)
    filename = '{}_text.png'.format(option.lower())
    tgi = TextGeneratedImage('{}/images/options/{}'.format(self.destination, filename), params)
    tgi.front = ''
    tgi.generate_image()
    return 'images/options/{}'.format(filename)


  def get_skip_text_code(self, option, tile):
    return '{}_text_{}'.format(option.lower(), tile)


  def flatten_images(self):
    for idx, option in enumerate(self.get_skips()):
      if isinstance(option['img'], TextGeneratedImage):
        self.skips[idx]['img'] = str(option['img'].get_path())


  def cut_apart_image(self, image):
    stream = popen('convert {}/{} -crop 4x1@ +repage +adjoin {}/{}_\%d.png'.format(self.destination, image, self.destination, image.replace('.png', '')))
    stream.read()


  def get_skips(self):
    if not self.skips:
      self.skips = []
      for option, data in self.load_skips().items():
        image_thing = self.get_skip_text_img(option, data['display_name'])
        self.cut_apart_image(image_thing)
        self.skips.append({
          'name': '{} Text'.format(data['display_name']),
          'type': 'static',
          'img': image_thing.replace('.png', '_0.png'),
          'codes': self.get_skip_text_code(option, 0)
        })
        self.skips.append({
          'name': '{} Text'.format(data['display_name']),
          'type': 'static',
          'img': image_thing.replace('.png', '_1.png'),
          'codes': self.get_skip_text_code(option, 1)
        })
        self.skips.append({
          'name': '{} Text'.format(data['display_name']),
          'type': 'static',
          'img': image_thing.replace('.png', '_2.png'),
          'codes': self.get_skip_text_code(option, 2)
        })
        self.skips.append({
          'name': '{} Text'.format(data['display_name']),
          'type': 'static',
          'img': image_thing.replace('.png', '_3.png'),
          'codes': self.get_skip_text_code(option, 3)
        })
        skip_button = {
          'name': data['display_name'],
          'type': 'toggle',
          'img': 'images/options/check_on.png',
          'disabled_img': 'images/options/check_off.png',
          'codes': option,
          'loop': True,
        }
        if 'default_state' in data:
          skip_button['initial_active_state'] = data['default_state']
        self.skips.append(skip_button)
    return self.skips