from os import popen
from yaml import safe_load
from image_utils.TextGeneratedImage import TextGeneratedImage

class GenerateOptions:

  def __init__(self, destination):
    self.options = None
    self.destination = destination


  def get_option_list(self):
    option_list = {}
    yamls = [
      'resources/rules/randomization.yaml',
    ]
    for yaml_file in yamls:
      with open(yaml_file, 'r') as ruleset:
        option_list.update(safe_load(ruleset))
    return option_list


  def get_option_text_code(self, option, tile):
    return '{}_text_{}'.format(option.lower(), tile)


  def get_image_thing(self, option, label):
    params = '-size 128x32 -background transparent -pointsize 15 -gravity east -fill white label:\'{}\''.format(label.replace('Randomize ', ''))
    tgi = TextGeneratedImage('{}/images/options/{}.png'.format(self.destination, option), params)
    tgi.front = ''
    tgi.generate_image()
    return 'images/options/{}.png'.format(option)


  def flatten_images(self):
    for idx, option in enumerate(self.get_options()):
      if isinstance(option['img'], TextGeneratedImage):
        self.options[idx]['img'] = str(option['img'].get_path())


  def cut_apart_image(self, image):
    stream = popen('convert {}/{} -crop 4x1@ +repage +adjoin {}/{}_\%d.png'.format(self.destination, image, self.destination, image.replace('.png', '')))
    stream.read()


  def get_options(self):
    if not self.options:
      self.options = []
      for option, data in self.get_option_list().items():
        image_thing = self.get_image_thing(option, data['display_name'])
        self.cut_apart_image(image_thing)
        self.options.append({
          'name': '{} Text 0'.format(data['display_name']),
          'type': 'static',
          'img': image_thing.replace('.png', '_0.png'),
          'codes': self.get_option_text_code(option, 0),
        })
        self.options.append({
          'name': '{} Text 1'.format(data['display_name']),
          'type': 'static',
          'img': image_thing.replace('.png', '_1.png'),
          'codes': self.get_option_text_code(option, 1),
        })
        self.options.append({
          'name': '{} Text 2'.format(data['display_name']),
          'type': 'static',
          'img': image_thing.replace('.png', '_2.png'),
          'codes': self.get_option_text_code(option, 2),
        })
        self.options.append({
          'name': '{} Text 3'.format(data['display_name']),
          'type': 'static',
          'img': image_thing.replace('.png', '_3.png'),
          'codes': self.get_option_text_code(option, 3),
        })
        option_json = {
          # If we don't have a display name, it really should have one ...
          # consider that exceptional enough to pop.
          'name': data['display_name'],
          'type': 'toggle',
          'codes': option,
          'img': 'images/options/check_on.png',
          'disabled_img': 'images/options/check_off.png',
          'loop': True,
        }
        if 'default_state' in data:
          option_json['initial_active_state'] = data['default_state']
        self.options.append(option_json)
      params = '-size 32x32 canvas:transparent'
      tgi = TextGeneratedImage('{}/images/options/empty_square.png'.format(self.destination), params)
      tgi.front = ''
      tgi.generate_image()
      self.options.append({
        "name": "Empty Square",
        "type": "static",
        "img": "images/options/empty_square.png",
        "codes": "empty_square",
      })
    return self.options