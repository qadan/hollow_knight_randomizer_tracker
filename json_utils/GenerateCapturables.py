from xml_utils.ItemXml import ItemXml

class GenerateCapturables:

  '''
  Generates an items JSON file to handle any items not defined as progression.
  '''

  capturable_types = [
    # Not 100% on whether anyone cares about arcane eggs, but given they're
    # worth a billion dollars someone might wanna come back for easy cash.
    'arcane_eggs',
    'charm_notches',
    'essence',
    'mask_shards',
    'pale_ores',
    'vessel_fragments',
  ]

  def __init__(self):
    self.capturables = []
    self.items = ItemXml()


  def get_name(self, item):
    item = item.replace('_', ' ')
    return item.replace('-', ' ')


  def get_charm_capturables(self):
    charm_capturables = []
    for item, data in self.items.get_items():
      if data['pool'] == 'Charm' and ('progression' not in data or not data['progression']):
        charm_capturables.append({
          'name': self.get_name(item),
          'type': 'toggle',
          'img': 'images/items/{}.png'.format(item.lower()),
          'codes': self.get_name(item),
        })
    return charm_capturables


  def get_capturables(self):
    if not self.capturables:
      for capturable_type in self.capturable_types:
        self.capturables.append({
          'name': capturable_type,
          'type': 'toggle',
          'img': 'images/items/{}.png'.format(capturable_type),
          'codes': capturable_type,
        })
      self.capturables.append(self.get_charm_capturables())
    return self.capturables