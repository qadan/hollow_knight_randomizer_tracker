from xml_utils.AdditiveXml import AdditiveXml
from xml_utils.ItemXml import ItemXml
from xml_utils.MacroXml import MacroXml
from xml_utils.ShopXml import ShopXml
from xml_utils.StartLocationXml import StartLocationXml
from xml_utils.WaypointXml import WaypointXml

'''
Little helper to just load all of the XML files in case we need e'm all.
'''

def aggregate_xml():
  aggregate_xml = {}
  source_objects = grouped_xml()
  for xml in source_objects.values():
    aggregate_xml.update(xml.get_items())
  return aggregate_xml


def grouped_xml():
  return {
    'additive': AdditiveXml(),
    'items': ItemXml(),
    'macros': MacroXml(),
    'shops': ShopXml(),
    'start_locations': StartLocationXml(),
    'waypoints': WaypointXml(),
  }
