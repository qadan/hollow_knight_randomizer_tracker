from xml_utils.xml_aggregator import grouped_xml
from yaml_utils.LocationYaml import LocationYaml

'''
Straight python port of the LogicManager from the rando. Doesn't include the
bits we don't want.

Essentially used to generate postifxes that are used by the Lua scripts to
determine accessibility.
'''

class LogicManager:

  def __init__(self):
    self.items = {}
    self.shops = {}
    self.additive_items = {}
    self.macros = {}
    self.start_locations = {}
    self.waypoints = {}
    self.skips = {}

    self.progression_indexed_items = {}
    self.pool_indexed_items = {}
    self.grub_progression = []
    self.essence_progression = []
    self.grubfather_locations = []
    self.seer_locations = []
    self.progression_items = []

    self.progression_bitmask = {}

    self.bitmask_max = 1
    self.essence_index = 0
    self.grub_index = 0

    self.xml_groups = grouped_xml()
    self.location_yaml = LocationYaml()



  def get_item_names(self):
    return self.items.keys()


  def get_shop_names(self):
    return self.shops.keys()


  def get_additive_item_names(self):
    return self.additive_items.keys()


  def get_additive_item_sets(self):
    return self.additive_items.values()


  def get_waypoints(self):
    return self.waypoints.keys()


  def get_start_locations(self):
    return self.start_locations.keys()


  def parse_xml(self):
    self.parse_additive_items()
    self.parse_macros()
    self.parse_item_xml()
    self.parse_shop_xml()
    self.parse_waypoint_xml()
    self.parse_start_location_xml()
    self.create_shortcuts()
    self.process_logic()


  def parse_additive_items(self):
    for item, data in self.xml_groups['additive'].get_items():
        self.additive_items[item] = data['itemName']
        self.macros[item] = self.shunting_yard(' | '.join(data['itemName']))


  def parse_macros(self):
    for item, data in self.xml_groups['macros'].get_items():
        self.macros[item] = self.shunting_yard(data['itemLogic'])
  

  def parse_item_xml(self):
    for item, data in self.xml_groups['items'].get_items():
        self.items[item] = data
        self.items[item]['itemLogic'] = self.shunting_yard(self.items[item]['itemLogic'])
        location = self.location_yaml.get_by_qualified_name(item)
        if location and 'check_infix' in location:
          self.items[item]['checkLogic'] = self.shunting_yard(location['check_infix'])


  def parse_shop_xml(self):
    for item, data in self.xml_groups['shops'].get_items():
        self.shops[item] = data
        self.shops[item]['itemLogic'] = self.shunting_yard(self.shops[item]['itemLogic'])


  def parse_waypoint_xml(self):
    for item, data in self.xml_groups['waypoints'].get_items():
        self.waypoints[item] = data
        self.waypoints[item]['itemLogic'] = self.shunting_yard(self.waypoints[item]['itemLogic'])


  def parse_start_location_xml(self):
    for item, data in self.xml_groups['start_locations'].get_items():
        self.start_locations[item] = data


  def create_shortcuts(self):
    for item in self.items.keys():
      if 'progression' in self.items[item] and self.items[item]['progression']:
        self.progression_items.append(item)
    for item in self.get_item_names():
      if 'progression' in self.items[item] and self.items[item]['progression']:
        self.progression_indexed_items[item] = []
      if self.items[item]['pool'] not in self.pool_indexed_items:
        self.pool_indexed_items[self.items[item]['pool']] = []
    for waypoint in self.get_waypoints():
      self.progression_indexed_items[waypoint] = []
    for item in self.get_item_names():
      for shunted in self.items[item]['itemLogic']:
        if shunted in self.progression_indexed_items:
          self.progression_indexed_items[shunted].append(item)
    for shop in self.get_shop_names():
      for shunted in self.shops[shop]['itemLogic']:
        if shunted in self.progression_indexed_items:
          self.progression_indexed_items[shunted].append(shop)


  def add_settings(self):
    self.skips['SHADESKIPS'] = (1, 1)
    self.skips['ACIDSKIPS'] = (2, 1)
    self.skips['SPIKETUNNELS'] = (4, 1)
    self.skips['SPICYSKIPS'] = (8, 1)
    self.skips['FIREBALLSKIPS'] = (16, 1)
    self.skips['DARKROOMS'] = (32, 1)
    self.skips['MILDSKIPS'] = (64, 1)
    self.skips['NOTCURSED'] = (128, 1)
    self.skips['CURSED'] = (256, 1)
    self.progression_bitmask['SHADESKIPS'] = (1, 1)
    self.progression_bitmask['ACIDSKIPS'] = (2, 1)
    self.progression_bitmask['SPIKETUNNELS'] = (4, 1)
    self.progression_bitmask['SPICYSKIPS'] = (8, 1)
    self.progression_bitmask['FIREBALLSKIPS'] = (16, 1)
    self.progression_bitmask['DARKROOMS'] = (32, 1)
    self.progression_bitmask['MILDSKIPS'] = (64, 1)
    self.progression_bitmask['NOTCURSED'] = (128, 1)
    self.progression_bitmask['CURSED'] = (256, 1)


  def process_shunted(self, shunted):
    postfix = []
    while shunted:
      val = shunted.pop()
      if val == '|':
        postfix.append((-1, 1))
      elif val == '+':
        postfix.append((-2, 1))
      elif val == 'ESSENCECOUNT':
        postfix.append((-3, 1))
      elif val == 'GRUBCOUNT':
        postfix.append((-4, 1))
      elif val == '200ESSENCE':
        postfix.append((-5, 1))
      else:
        postfix.append(self.progression_bitmask[val])
    # Reversing the postfix is immensely faster than performing prepends to the
    # stack, and ensures the interpreter Lua can also perform quickly using a
    # plain ol' for loop.
    postfix.reverse()
    return postfix


  def process_logic(self):
    self.add_settings()

    idx = 9

    for item in self.get_item_names():
      if 'progression' in self.items[item] and self.items[item]['progression']:
        self.progression_bitmask[item] = (2 ** idx, self.bitmask_max)
        idx += 1
        if idx == 31:
          idx = 0
          self.bitmask_max += 1

    for shop in self.get_shop_names():
      self.progression_bitmask[shop] = (2 ** idx, self.bitmask_max)
      idx += 1
      if idx == 31:
        idx = 0
        self.bitmask_max += 1

    for waypoint in self.get_waypoints():
      self.progression_bitmask[waypoint] = (2 ** idx, self.bitmask_max)
      idx += 1
      if idx == 31:
        idx = 0
        self.bitmask_max += 1

    self.essence_index = self.bitmask_max + 1
    self.grub_index = self.bitmask_max + 2
    self.bitmask_max = self.grub_index

    for item in self.get_item_names():
      self.items[item]['processedItemLogic'] = self.process_shunted(self.items[item]['itemLogic'])
      if 'checkLogic' in self.items[item]:
        self.items[item]['processedCheckLogic'] = self.process_shunted(self.items[item]['checkLogic'])

    for shop in self.get_shop_names():
      self.shops[shop]['processedItemLogic'] = self.process_shunted(self.shops[shop]['itemLogic'])

    for waypoint in self.get_waypoints():
      self.waypoints[waypoint]['processedItemLogic'] = self.process_shunted(self.waypoints[waypoint]['itemLogic'])


  def shunting_yard(self, infix):
    idx = 0
    stack = []
    postfix = []

    while idx < len(infix):
      next_op, new_idx = self.get_next_operator(infix, idx)
      idx = new_idx
      if next_op.strip() == '':
        continue
      if next_op in ['+', '|']:
        while (len(stack) != 0 and next_op not in ['+', '|'] and stack[-1] != '|') and stack[-1] != '(':
          postfix.append(stack.pop())
        stack.append(next_op)
      elif next_op == '(':
        stack.append(next_op)
      elif next_op == ')':
        while stack[-1] != '(':
          postfix.append(stack.pop())
        stack.pop()
      else:
        if next_op in self.macros:
          postfix.extend(self.macros[next_op])
        else:
          postfix.append(next_op)
    for op in range(len(stack)):
      postfix.append(stack.pop())

    return postfix


  def get_next_operator(self, infix, idx):
    start = idx
    operators = ['(', ')', '+', '|']
    if infix[idx] in operators:
      idx += 1
      return (infix[idx - 1], idx)
    while idx < len(infix) and infix[idx] not in operators:
      idx += 1
    return (infix[start:idx].strip(), idx)
