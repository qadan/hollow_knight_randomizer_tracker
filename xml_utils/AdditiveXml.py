from xml_utils.AbstractXml import AbstractXml

class AdditiveXml(AbstractXml):

  def get_item_xpath(self):
    return './additiveItemSet'


  def get_xml_filename(self):
    return 'additive.xml'


  def get_additive_group(self, item):
    if not self.items:
      self.parse_items()
    for name, additives in self.items.items():
      if item in additives['itemName']:
        return (name, additives['itemName'])
    return None


  def parse_items(self):
    '''
    The items in an additive set should be a list in order.
    '''
    self.items = {}
    items = self.xml.getroot().findall(self.get_item_xpath())
    for item in items:
      self.items[item.attrib['name']] = {
        'itemName': [],
      }
      for child in item:
        self.items[item.attrib['name']]['itemName'].append(child.text)
      self.items[item.attrib['name']]['_source'] = self.get_xml_filename()