import re
from xml_utils.AbstractXml import AbstractXml

class StartLocationXml(AbstractXml):

  def get_item_xpath(self):
    return './start'


  def get_xml_filename(self):
    return 'startlocations.xml'


  def parse_items(self):
    super().parse_items()
    '''
    The logic to access a waypoint is self reflective.
    '''
    for item, attributes in self.items.items():
      self.items[item]['itemLogic'] = attributes['waypoint']
      self.items[item]['cleanName'] = ''.join(filter(str.isalpha, item))


  def get_item_by_waypoint(self, waypoint):
    if not self.items:
      self.parse_items()
    for item, attributes in self.items.items():
      if attributes['waypoint'] == waypoint:
        return self.items[item]
