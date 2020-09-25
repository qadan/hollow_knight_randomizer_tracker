from xml_utils.AbstractXml import AbstractXml

class MacroXml(AbstractXml):

  def get_item_xpath(self):
    return './macro'


  def get_xml_filename(self):
    return 'macros.xml'


  def parse_items(self):
    '''
    Not all of the macros are actually useful here and should be parsed; most
    of them are specifically used in door randomizer, and should be skipped.
    This is a little hack-y but I don't want to process unnecessary stuff.
    '''
    self.items = {}
    items = self.xml.getroot().findall(self.get_item_xpath())
    for item in items:
      # Room rando macros are named after the room or have '-R' appended.
      if (item.attrib['name'].isupper() and item.attrib['name'][-2:] != '-R'):
        self.items[item.attrib['name']] = {
          'itemLogic': item.text,
          '_source': self.get_xml_filename()
        }