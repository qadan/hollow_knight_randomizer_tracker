from logic_utils.LogicManager import LogicManager
from yaml_utils.LocationYaml import LocationYaml

class GenerateBitmaskedLocations:

  relic_types = [
    'hallownest_seals',
    'arcane_eggs',
    'wanderers_journals',
    'kings_idols',
  ]

  checkable_groups = [
    'seer',
    'grubfather',
  ]

  capturable_types = [
    'whispering_roots',
  ]

  def __init__(self):
    self.location_yaml = LocationYaml()
    self.locations = []


  def bitmask_access_rules(self, location):
    if location == 'stag_nest':
      return '$can_get_waypoint|{}'.format(location)
    if location in self.checkable_groups:
      return '{{$can_get_item|{}}}'.format(location)
    return '$can_get_item|{}'.format(location)


  def bitmask_check_rules(self, location):
    return '{{$can_check_item|{}}}'.format(location)


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
        "name": "Sly (maximum {} items)".format(len(sly_parts_of)),
        "group": "sly",
        "clear_as_group": False,
        "item_count": len(sly_parts_of),
        "access_rules": [self.bitmask_access_rules('sly')],
        "capture_item": True,
        "capture_item_layout": 'item_grid_tall',
      },
      {
        "name": "Sly (Shopkeeper's Key; maximum {} additional items)".format(len(sly_key_parts_of)),
        "group": "sly_key",
        "clear_as_group": False,
        "item_count": len(sly_key_parts_of),
        "access_rules": [self.bitmask_access_rules('sly_key')],
        "capture_item": True,
        "capture_item_layout": 'item_grid_tall',
      },
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
    if data['group_type'] == 'slys_special_magical_goddamn_group':
      definition['sections'].extend(self.get_sly_sections())
      definition['map_locations'][0]['visibility_rules'] = ['randomize_shops']
    else:
      for part_loc, part_data in parts_of.items():
        part_type = 'relics' if part_data['type'] in self.relic_types else part_data['type']
        definition['sections'].append({
          'name': self.location_yaml.get_display_name(part_loc),
          'item_count': 1,
          'access_rules': ['randomize_{},{}'.format(part_type, self.bitmask_access_rules(location) if data['type'] == 'shops' else self.bitmask_access_rules(part_loc))],
          'capture_item': part_type in self.capturable_types or data['group_type'] == 'group',
          'capture_item_layout': 'item_grid_tall',
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
        loc_type = data['type'] if data['type'] not in self.relic_types else 'relics'
        access_rules = [self.bitmask_access_rules(location)]
        if 'check_infix' in data:
          access_rules.append(self.bitmask_check_rules(location))
        self.locations.append({
          'name': self.location_yaml.get_display_name(location),
          'map_locations': [{
            'map': 'hallownest',
            'x': data['x_coord'],
            'y': data['y_coord'],
            'size': 50,
            'visibility_rules': ['randomize_{}'.format(loc_type)]
          }],
          'sections': [{
            'name': data['description'] if 'description' in data else self.location_yaml.get_display_name(location),
            'access_rules': access_rules,
            'item_count': 1,
            'capture_item': loc_type in self.capturable_types,
            'capture_item_layout': 'item_grid_tall',
          }],
        })
    return self.locations
