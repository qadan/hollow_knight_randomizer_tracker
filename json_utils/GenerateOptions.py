from yaml import safe_load
from image_utils.TextGeneratedImage import TextGeneratedImage
from image_utils.ResourceIncludedImage import ResourceIncludedImage

class GenerateOptions:

  def __init__(self, destination):
    self.options = None
    self.destination = destination


  def get_option_list(self):
    option_list = {}
    yamls = [
      'resources/rules/randomization.yaml',
      'resources/rules/skips.yaml',
    ]
    for yaml_file in yamls:
      with open(yaml_file, 'r') as ruleset:
        option_list.update(safe_load(ruleset))
    return option_list


  def on_params(self, location):
    return '-size 32x32 -background blue -gravity center -fill white label:\'{}\''.format(location, location)


  def off_params(self, location):
    return '-size 32x32 -background transparent -gravity center -fill white label:\'{}\''.format(location, location)


  def get_image_thing(self, option, data, on=True):
    if 'image' in data:
      image = ResourceIncludedImage('resources/images/items/{}'.format(data['image']))
      destination = '{}/images/items/{}'.format(self.destination, data['image'])
      image.copy_the_thing('{}/images/items/{}'.format(self.destination, data['image']))
      return 'images/items/{}'.format(data['image'])
    display_name = data['display_name'][10:] if data['display_name'].startswith('Randomize ') else data['display_name']
    lb = display_name.replace(' ', '\n')
    im_params = self.on_params(lb) if on else self.off_params(lb)
    tgi = TextGeneratedImage('options/{}_{}.png'.format(option, 'on' if on else 'off'), im_params)
    tgi.front = 'resources/images'
    tgi.generate_image()
    return tgi


  def flatten_images(self):
    for idx, option in enumerate(self.get_options()):
      if isinstance(option['img'], TextGeneratedImage):
        self.options[idx]['img'].front = 'images'
        self.options[idx]['img'] = str(option['img'].get_path())
      if isinstance(option['img_off'], TextGeneratedImage):
        self.options[idx]['img_off'].front = 'images'
        self.options[idx]['img_off'] = str(option['img_off'].get_path())


  def get_options(self):
    if not self.options:
      self.options = []
      for option, data in self.get_option_list().items():
        option_json = {
          # If we don't have a display name, it really should have one ...
          # consider that exceptional enough to pop.
          'name': data['display_name'],
          'type': 'toggle',
          'img_off': self.get_image_thing(option, data, on=False),
          'img': self.get_image_thing(option, data),
          'codes': option,
        }
        if 'default_state' in data:
          option_json['initial_active_state'] = data['default_state']
        self.options.append(option_json)
    return self.options