from xml_utils.AbstractXml import AbstractXml

class ShopXml(AbstractXml):

  def get_item_xpath(self):
    return './shop'


  def get_xml_filename(self):
    return 'shops.xml'