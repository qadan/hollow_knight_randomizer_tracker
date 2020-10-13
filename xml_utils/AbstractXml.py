import abc
from logic_utils.NestedParentheticals import NestedParentheticals
import xml.etree.ElementTree as ET
from yaml_utils import settings
from pathlib import Path

class AbstractXml:

  '''
  Abstraction class for XML utilities. Any XML we need from the main randomizer
  will require functionality defined here.
  '''

  def __init__(self):
    self.xml = ET.parse(Path(settings.get_mod_path(), 'Resources', self.get_xml_filename()).open(mode='r'))
    self.items = None
    self.qualified_names = None


  def get_items(self):
    if self.items is None:
      self.parse_items()
    return self.items.items()


  def parse_items(self):
    self.items = {}
    items = self.xml.getroot().findall(self.get_item_xpath())
    for item in items:
      self.items[item.attrib['name']] = {}
      for child in item:
        if not child.text:
          if child.tag == 'itemLogic':
            text = []
          else:
            text = None
        elif child.text == 'true':
          text = True
        elif child.text == 'false':
          text = False
        elif child.text.isdigit():
          text = int(child.text)
        else:
          text = child.text
        self.items[item.attrib['name']][child.tag] = text
      self.items[item.attrib['name']]['_source'] = self.get_xml_filename()



  def get_qualified_names(self):
    return self.get_items().keys()


  def get_by_qualified_name(self, name):
    self.get_items()
    if name in self.items:
      return self.items[name]
    return None


  @abc.abstractmethod
  def get_item_xpath(self):
    '''
    Subclasses must define the XPath to target the list of individual items.
    '''
    pass


  @abc.abstractmethod
  def get_xml_filename(self):
    '''
    Subclasses must define the name of the XML file in the main randomizer's
    resources folder.
    '''
    pass
