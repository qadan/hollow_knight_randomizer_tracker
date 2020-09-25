import argparse
import sys
from xml_utils.ItemXml import ItemXml
from xml_utils.ShopXml import ShopXml
from yaml_utils.LocationYaml import LocationYaml

class ValidateLocationYaml(object):

  def __init__(self):
    self.yaml = LocationYaml()
    self.item_xml = ItemXml()
    self.shop_xml = ShopXml()


  def validate_will_place_coords(self):
    '''
    Validate that each entry in the .yaml has either an x_coord and y_coord, or
    that it implements a part_of.
    '''
    for location, attributes in self.yaml.get_aggregate_locations().items():
      if 'part_of' not in attributes:
        assert 'x_coord' in attributes, "{} ({}) does not implement part_of and is missing x_coord".format(location, attributes['_source_yaml'])
        assert 'y_coord' in attributes, "{} ({}) does not implement part_of and is missing y_coord".format(location, attributes['_source_yaml'])
      else:
        assert 'x_coord' not in attributes, "{} ({}) implements part_of but also x_coord".format(location, attributes['_source_yaml'])
        assert 'y_coord' not in attributes, "{} ({}) implements part_of but also y_coord".format(location, attributes['_source_yaml'])


  def validate_coords(self):
    '''
    Validate that x_coords and y_coords are integers that fit on the map.
    '''
    for location, attributes in self.yaml.get_aggregate_locations().items():
      if 'part_of' not in attributes:
        assert isinstance(attributes['x_coord'], int), "The x_coord of {} ({}) is not an integer.".format(location, attributes['_source_yaml'])
        assert isinstance(attributes['y_coord'], int), "The y_coord of {} ({}) is not an integer.".format(location, attributes['_source_yaml'])
        assert 0 <= attributes['x_coord'] <= self.yaml.MAP_WIDTH, "The x_coord of {} ({}) does not fit within the bounds of the map.".format(location, attributes['_source_yaml'])
        assert 0 <= attributes['y_coord'] <= self.yaml.MAP_HEIGHT, "The y_coord of {} ({}) does not fit within the bounds of the map.".format(location, attributes['_source_yaml'])


  def validate_parents(self):
    '''
    Validate that each part_of can be traced back to a parent.
    '''
    parents = self.yaml.get_parents()
    for parent in self.yaml.get_parents():
      # Some dummy items can be part_of nothing and require no coordinates.
      if parent is not None:
        assert parent in self.yaml.get_aggregate_locations(), "Items reference part_of {}, which does not exist.".format(parent)


  def validate_has_qualified_name(self):
    '''
    Validate that each location has a qualified_name.
    '''
    for location, attributes in self.yaml.get_aggregate_locations().items():
      # Reference locations don't need qualified names.
      if attributes['type'] != 'reference_locations':
        assert 'qualified_name' in attributes, "{} ({}) has no qualified_name.".format(location, attributes['_source_yaml'])


  def validate_no_duplicate_qualified_names(self):
    '''
    No qualified name should appear in the yamls twice.
    '''
    qualified_names = self.yaml.get_qualified_names()
    iterated = set()
    iterated_twice = list(set(item for item in qualified_names if item in iterated or iterated.add(item)))
    assert not iterated_twice, "Duplicate qualified_names found: {}".format(str(iterated_twice))


  def validate_qualified_name_representation(self):
    '''
    All qualified names should be represented in the XML.
    '''
    qualified_names = self.yaml.get_qualified_names()
    for name in qualified_names:
      assert self.shop_xml.get_by_qualified_name(name) or self.item_xml.get_by_qualified_name(name), "{} is represented in the yaml qualified names but not in the XML.".format(name)


  def validate_xml_representation(self):
    exempt_names = self.yaml.get_exempt_qualified_names()
    for name in self.shop_xml.get_qualified_names():
      if name not in exempt_names:
        assert self.yaml.get_by_qualified_name(name), "{} is represented in the shop XML qualified names but not in the YAML.".format(name)
    for name in self.item_xml.get_qualified_names():
      if name not in exempt_names:
        assert self.yaml.get_by_qualified_name(name), "{} is represented in the item XML qualified names but not in the YAML.".format(name)


  def validate_location_yaml(self):
    '''
    We want to validate the following things:
    - There should be a 1:1 ratio between qualified_name entries and XML items.
    '''
    self.validate_will_place_coords()
    self.validate_coords()
    self.validate_parents()
    self.validate_has_qualified_name()
    self.validate_no_duplicate_qualified_names()
    self.validate_qualified_name_representation()
    self.validate_xml_representation()