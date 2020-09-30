from string import ascii_lowercase
from yaml import safe_load
from pathlib import Path
from image_utils.TextGeneratedImage import TextGeneratedImage

class GenerateStartLocations:

  def __init__(self):
    self.start_locations = {
      "name": "Starting Point",
      "type": "progressive",
      "loop": True,
      "stages": [],
      "initial_stage_idx": 0,
      "codes": "starting_location",
      "allow_disabled": False,
    }
    self.start_location_icon = {
      "name": "Starting Point Icon",
      "type": "static",
      "codes": "starting_point_icon",
      "img": TextGeneratedImage('options/starting_point_icon.png', '-background transparent -size 32x32 -fill white -gravity center label:\'Start\\nLoc:\'')
    }
    self.loaded_yaml = None


  def get_image_config(self, text):
    return '-background transparent -size 160x32 -pointsize 16 -fill white -gravity center -bordercolor gray50 -border 1x1 label:\'{}\''.format(text)


  def get_icon_text(self, location):
    return ''.join([bit[0] for bit in location.split('_') if bit[0] in ascii_lowercase]).upper()


  def get_starting_point_yaml(self):
    if not self.loaded_yaml:
      with open(Path('resources/rules/starting_points.yaml'), 'r') as starting_point_yaml:
        self.loaded_yaml = safe_load(starting_point_yaml)
    return self.loaded_yaml


  def generate_start_locations(self):
    starting_points = self.get_starting_point_yaml()['starting_points']
    for location, data in starting_points.items():
      icon_text = self.get_icon_text(location)
      self.start_locations['stages'].append({
        'codes': "starting_location,{}".format(data['as'] if 'as' in data else location),
        'inherit_codes': False,
        'img': TextGeneratedImage('options/starting_point_{}.png'.format(location), self.get_image_config(data['display_label'])),
      })
    return self.start_locations


  def get_start_locations(self):
    if not self.start_locations['stages']:
      self.generate_start_locations()
    return [self.start_locations, self.start_location_icon]


  def generate_images(self, front):
    for img in self.get_start_locations()[0]['stages']:
      if isinstance(img['img'], TextGeneratedImage):
        img['img'].front = '{}/images'.format(front)
        img['img'].generate_image()
    if isinstance(self.get_start_locations()[1]['img'], TextGeneratedImage):
      self.start_location_icon['img'].front = '{}/images'.format(front)
      self.start_location_icon['img'].generate_image()


  def flatten_images(self):
    for idx, stage in enumerate(self.get_start_locations()[0]['stages']):
      if isinstance(stage['img'], TextGeneratedImage):
        self.start_locations['stages'][idx]['img'].front = 'images'
        self.start_locations['stages'][idx]['img'] = str(stage['img'].get_path())
    if isinstance(self.get_start_locations()[1]['img'], TextGeneratedImage):
      self.start_location_icon['img'].front = 'images'
      self.start_location_icon['img'] = str(self.start_location_icon['img'].get_path())