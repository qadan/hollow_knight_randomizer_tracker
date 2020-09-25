from xml_utils.AbstractXml import AbstractXml

class ItemXml(AbstractXml):

  def get_item_xpath(self):
    return './item'


  def get_xml_filename(self):
    return 'items.xml'