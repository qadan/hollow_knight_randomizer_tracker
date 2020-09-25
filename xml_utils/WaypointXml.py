from xml_utils.AbstractXml import AbstractXml

class WaypointXml(AbstractXml):

  def get_item_xpath(self):
    return './item'


  def get_xml_filename(self):
    return 'waypoints.xml'


  def parse_items(self):
    super().parse_items()
    for item, attributes in self.items.items():
      self.items[item]['cleanName'] = ''.join(filter(lambda char: str.isalpha(char) or str.isnumeric(char) or char == '_', item)).lower()