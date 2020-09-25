from pathlib import Path
from yaml import safe_load, parser
from image_utils.ResourceIncludedImage import ResourceIncludedImage

class LocationYaml(object):

  '''
  The internal .yaml in the resources/locations folder contains information
  specific to the tracker (like x/y coordinates and grouping information).
  '''

  MAP_WIDTH = 4177
  MAP_HEIGHT = 2757
  IMAGE_SOURCE_MOD = 'mod'
  IMAGE_SOURCE_RESOURCES = 'resources'

  def __init__(self):
    self.aggregate_locations = None
    self.parents = None


  def get_yaml_file_list(self):
    return [
      Path('resources/locations/arcane_eggs.yaml'),
      Path('resources/locations/charm_notches.yaml'),
      Path('resources/locations/charms.yaml'),
      Path('resources/locations/dreamers.yaml'),
      Path('resources/locations/essence_bosses.yaml'),
      Path('resources/locations/geo_chests.yaml'),
      Path('resources/locations/grubs.yaml'),
      Path('resources/locations/hallownest_seals.yaml'),
      Path('resources/locations/keys.yaml'),
      Path('resources/locations/kings_idols.yaml'),
      Path('resources/locations/maps.yaml'),
      Path('resources/locations/mask_shards.yaml'),
      Path('resources/locations/pale_ores.yaml'),
      Path('resources/locations/rancid_eggs.yaml'),
      Path('resources/locations/reference_locations.yaml'),
      Path('resources/locations/shops.yaml'),
      Path('resources/locations/skills.yaml'),
      Path('resources/locations/stag_stations.yaml'),
      Path('resources/locations/vessel_fragments.yaml'),
      Path('resources/locations/wanderers_journals.yaml'),
      Path('resources/locations/whispering_roots.yaml'),
    ]


  def get_aggregate_locations(self):
    if self.aggregate_locations is None:
      self.aggregate_locations = {}
      yaml_files = self.get_yaml_file_list()
      for file in yaml_files:
        with file.open() as stream:
          try:
            locations = safe_load(stream)
          except parser.ParserError as e:
            print('Failed to load {}: {}'.format(file, e))
          location_type = next(iter(locations))
          for location, attributes in locations[location_type].items():
            self.aggregate_locations[location] = attributes
            self.aggregate_locations[location]['_source_yaml'] = file.name
            self.aggregate_locations[location]['type'] = location_type
            self.aggregate_locations[location]['location_name'] = location
    return self.aggregate_locations


  def get_locations(self, location_type):
    return [location for location in self.get_aggregate_locations().values() if location['type'] == location_type]


  def get_locations_with_parents(self):
    locations_with_parents = {}
    for location, attributes in self.get_aggregate_locations().items():
      if 'part_of' in attributes:
        yield (location, attributes)


  def get_parents(self):
    if self.parents is None:
      self.parents = []
      for location, attributes in self.get_aggregate_locations().items():
        if 'part_of' in attributes and attributes['part_of'] not in self.parents:
          self.parents.append(attributes['part_of'])
    return self.parents


  def get_qualified_names(self):
    qualified_names = []
    for location, attributes in self.get_aggregate_locations().items():
      if 'qualified_name' in attributes:
        qualified_names.append(attributes['qualified_name'])
    return qualified_names


  def get_exempt_qualified_names(self):
    return [
      'Focus',
      '1_Geo',
      'Grub-Ruins2_11(1)',
      'Grub-Ruins2_11(2)',
      'Equipped',
      'Placeholder',
    ]


  def get_by_qualified_name(self, name):
    if name in self.get_exempt_qualified_names():
      return None
    for location, attributes in self.get_aggregate_locations().items():
      if 'qualified_name' in attributes and attributes['qualified_name'] == name:
        return attributes


  def get_by_index(self, index):
    return self.get_aggregate_locations()[index]


  def get_display_name(self, index):
    location = self.get_aggregate_locations()[index]
    if 'display_name' in location:
      return location['display_name']
    return self.get_default_display_name(location['type'])


  def get_default_display_name(self, location_type):
    default_display_names = {
      'arcane_eggs': 'Arcane Egg',
      'charm_notches': 'Charm Notch',
      'geo_chests': 'Geo Chest',
      'grubs': 'Grub',
      'hallownest_seals': 'Hallownest Seal',
      'kings_idols': 'King\'s Idol',
      'mask_shards': 'Mask Shard',
      'pale_ores': 'Pale Ore',
      'rancid_eggs': 'Rancid Egg',
      'vessel_fragments': 'Vessel Fragment',
      'wanderers_journals': 'Wanderer\'s Journal',
      'whispering_roots': 'Whispering Root',
    }
    if location_type in default_display_names.keys():
      return default_display_names[location_type]
    return ''


  def get_count(self, location):
    if 'count' in location:
      return location['count']
    return 1


  def get_parts_of(self, location):
    parts_of = {}
    for child, data in self.get_aggregate_locations().items():
      if 'part_of' in data and data['part_of'] == location:
        parts_of[child] = data
    return parts_of


  def captures_location(self, loc_type):
    return loc_type in [
      'whispering_roots',
    ]
