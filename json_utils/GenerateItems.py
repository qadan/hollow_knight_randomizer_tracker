from image_utils.ResourceIncludedImage import ResourceIncludedImage
from xml_utils.ItemXml import ItemXml
from xml_utils.AdditiveXml import AdditiveXml
from yaml_utils import settings
from yaml_utils.LocationYaml import LocationYaml

class GenerateItems:

  def __init__(self):
    self.item_xml = ItemXml()
    self.additive_xml = AdditiveXml()
    self.locations = LocationYaml()
    self.items = None


  def generate_additive_group(self, additive):
    qualified_name, data = additive
    first = data[0]
    del data[0]
    yaml_info = self.locations.get_by_qualified_name(first)
    # Progression items should have been given a display name ... if it's
    # missing one, consider that an exceptional state and halt execution.
    image = "images/items/{}.png".format(yaml_info['location_name'])
    additive_group = {
      'name': self.locations.get_display_name(yaml_info['location_name']),
      'type': 'progressive',
      'allow_disabled': False,
      'stages': [
        {
          'img': image,
          'img_mods': '@disabled',
        },
        {
          'img': image,
          'codes': yaml_info['location_name'],
          'inherit_codes': True,
        }
      ]
    }
    for item_name in data:
      yaml_info = self.locations.get_by_qualified_name(item_name)
      to_append = {
        'img': "images/items/{}.png".format(yaml_info['location_name']),
        'codes': yaml_info['location_name'],
        'inherit_codes': True,
      }
      additive_group['stages'].append(to_append)
    return additive_group


  def generate_individual_item(self, name, data):
    yaml_info = self.locations.get_by_qualified_name(name)
    return {
      'name': self.locations.get_display_name(yaml_info['location_name']),
      'type': 'toggle',
      'img': 'images/items/{}.png'.format(yaml_info['location_name']),
      'codes': yaml_info['location_name'],
      'allow_disabled': False,
    }

  def is_exempt(self, name):
    exempt_things = self.locations.get_exempt_qualified_names()
    exempt_things.extend(['Dreamer', 'Seer', 'Grubfather'])
    return name in exempt_things or name.startswith('Grub-') or name.startswith('Whispering_Root-') or name.startswith('Simple_Key-')


  def generate_items(self):
    if not self.items:
      additives_added = []
      # Start out with grub count and simple keys, which we won't generate on
      # the fly.
      self.items = [
        {
          'name': 'Grubs',
          'type': 'consumable', # lol
          'img': 'images/items/grub.png',
          'max_quantity': 46,
          'codes': 'grubs',
          'allow_disabled': False,
        },
        {
          'name': 'Simple Key',
          'type': "consumable",
          'img': 'images/items/simple_key.png',
          'max_quantity': 4,
          'codes': 'simple_key',
          'allow_disabled': False,
        },
        # Add in the fourth dreamer. This one's a weird case where we have an
        # item that isn't attached to an original location, so hacking it in.
        {
          'name': 'Dreamer',
          'type': 'toggle',
          'img': 'images/items/dreamer.png',
          'codes': 'dreamer',
          'allow_disabled': False,
        }
      ]
      for name, data in self.item_xml.get_items():
        if name not in additives_added:
          additive = self.additive_xml.get_additive_group(name)
          if additive is not None:
            additives_added.extend(additive[1])
            self.items.append(self.generate_additive_group(additive))
          elif 'progression' in data and data['progression'] and not self.is_exempt(name):
            self.items.append(self.generate_individual_item(name, data))
      # Hack in the sub-images for stag stations.
      for idx, item in enumerate(self.items):
        if 'codes' in item and item['codes'].endswith('_stag'):
          self.items[idx]['img'] = 'images/items/stag_station.png'
          self.items[idx]['img_mods'] = 'overlay|images/overlays/{}_overlay.png'.format(item['codes'])
    return self.items
