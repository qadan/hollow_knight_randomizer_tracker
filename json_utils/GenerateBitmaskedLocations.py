from logic_utils.LogicManager import LogicManager
from yaml_utils.LocationYaml import LocationYaml

class GenerateBitmaskedLocations:

  def __init__(self):
    self.location_yaml = LocationYaml()
    self.locations = []


  def bitmask_access_rules(self, randomization_type, location):
    if randomization_type == 'reference_locations':
      return '$can_get_waypoint|{}'.format(location)
    if randomization_type in ['hallownest_seals', 'arcane_eggs', 'wanderers_journals', 'kings_idols']:
      randomization_type = 'relics'
    return 'randomize_{},$can_get_item|{}'.format(randomization_type, location)


  def get_locations(self):
    self.generate_locations()
    return [{
      'name': 'Hallownest',
      'children': self.locations,
    }]


  def get_sly_sections(self):
    sly_parts_of = self.location_yaml.get_parts_of('sly')
    sly_key_parts_of = self.location_yaml.get_parts_of('sly_key')
    return [
      {
        "name": "Sly",
        "group": "sly",
        "clear_as_group": False,
        "item_count": len(sly_parts_of),
        "access_rules": [self.bitmask_access_rules('shops', 'sly')],
      },
      {
        "name": "Sly (Shopkeeper's Key)",
        "group": "sly_key",
        "clear_as_group": False,
        "item_count": len(sly_key_parts_of),
        "access_rules": [self.bitmask_access_rules('shops', 'sly_key')],
      },
      {
        "name": "Nailmaster's Glory",
        "group": "sly_basement",
        "item_count": 1,
        "access_rules": [self.bitmask_access_rules('charms', 'nailmasters_glory')],
      }
    ]


  def get_group_definition(self, location, data):
    definition = {
      'name': self.location_yaml.get_display_name(location),
      'group': location,
      'map_locations': [{
        'map': 'hallownest',
        'x': data['x_coord'],
        'y': data['y_coord'],
        'size': 50,
      }],
    }
    parts_of = self.location_yaml.get_parts_of(location)
    definition['sections'] = []
    if data['group_type'] == 'group':
      definition['sections'].append({
        'name': self.location_yaml.get_display_name(location),
        'group': location,
        'item_count': len(parts_of),
        "clear_as_group": False,
        'access_rules': [self.bitmask_access_rules(data['type'], location)]
      })
    elif data['group_type'] == 'slys_special_magical_goddamn_group':
      definition['sections'].extend(self.get_sly_sections())
    else:
      for part_loc, part_data in parts_of.items():
        definition['sections'].append({
          'name': self.location_yaml.get_display_name(part_loc),
          'item_count': 1,
          'access_rules': [self.bitmask_access_rules(self.location_yaml.get_aggregate_locations()[part_loc]['type'], part_loc)],
        })
    return definition


  def generate_locations(self):
    self.locations = []
    for location, data in self.location_yaml.get_aggregate_locations().items():
      if 'part_of' in data:
        continue
      elif 'group_type' in data:
        self.locations.append(self.get_group_definition(location, data))
      else:
        self.locations.append({
          'name': self.location_yaml.get_display_name(location),
          'map_locations': [{
            'map': 'hallownest',
            'x': data['x_coord'],
            'y': data['y_coord'],
            'size': 50,
          }],
          'sections': [{
            'name': data['description'] if 'description' in data else self.location_yaml.get_display_name(location),
            'access_rules': [self.bitmask_access_rules(data['type'], location)],
            'item_count': 1,
          }]
        })
    return self.locations