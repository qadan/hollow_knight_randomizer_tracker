from logic_utils.LogicManager import LogicManager

class GenerateLogicLua:

  '''
  Helper class for doing the thing your CS professor told you never to do.

  Listen, this isn't production code working with sensitive data, it's fine.

  This saves me from having to abstract this data through something like JSON
  and load a library to read from it. The resultant file is very large, has a
  lot of stuff in it, gets read very frequently, and benefits from existing
  natively in Lua.
  '''

  def __init__(self):
    self.logic_manager = LogicManager()
    self.logic_manager.parse_xml()
    self.lines = []
    self.destination = 'resources/static_lua/bitmasks.lua'


  def set_header(self):
    self.lines.extend([
      '----',
      '-- SOME DOCUMENTATION ON WHAT THE HELL YOU\'RE LOOKING AT:',
      '--',
      '-- The Hollow Knight Randomizer tracks logic on a graph of over 80 nodes, with',
      '-- hundreds of vertices, and enough Hamiltonian cycles to choke an Aaron Burr.',
      '-- Compounding this issue is the fact that you can start from one of 23 of those',
      '-- nodes, meaning that even if you could untangle the absolute mess of moving',
      '-- between locations, you would have to redo it 22 times from 22 starts.',
      '--',
      '-- Hollow Knight Randomizer\'s solution is to represent every location as a bit',
      '-- in a series of bitmasks. Location logic is represented in the randomizer as',
      '-- an infixed logical equation that can be converted into bitmasks we can check',
      '-- logic against. Your current accessibility is represented as a series of',
      '-- numbers, bitwise or\'d from individual item/waypoint values, that can be',
      '-- bitwise and\'d against to test access. This way, we can brute force a',
      '-- limited set of repeated checks against the nodes, perhaps opening new ones',
      '-- on each pass, without really having to calculate how they connect together.',
      '--',
      '-- Since the tracker understands that kind of logic, we can procedurally',
      '-- generate it from the actual randomizer code itself. As a result, it works',
      '-- regardless of starting point, and is resilient to future updates.',
      '----',
    ])


  def append_item(self, item, data, add_tracking):
    self.lines.append("  {} = {{".format(self.clean_name(item)))
    if item in self.logic_manager.progression_bitmask.keys():
      self.lines.append("    bitmask = {},".format(self.logic_manager.progression_bitmask[item][0]))
      self.lines.append("    group = {},".format(self.logic_manager.progression_bitmask[item][1]))
    if not data['processedItemLogic']:
      self.lines.append("    postfix = {},")
    else:
      self.lines.append("    postfix = {")
      for postfix in data['processedItemLogic']:
        self.lines.append("      {{{}, {}}},".format(postfix[0], postfix[1]))
      self.lines.append("    },")
    if add_tracking:
      self.lines.append("    status = 0,")
    self.lines.append("  },")


  def add_locations(self):
    self.lines.append("ITEM_TABLE = {")
    for item, data in self.logic_manager.items.items():
      self.append_item(item, data, False)
    for item, data in self.logic_manager.shops.items():
      self.append_item(item, data, False)
    self.lines.append("}")


  def add_space(self):
    self.lines.append('')
    self.lines.append('')


  def clean_name(self, item_name):
    # Trim numbers off of geo chest names.
    if item_name == '1_Geo':
      item_name = 'geo_1'
    elif '_Geo-' in item_name:
      item_name = item_name.split('_Geo-', 1)[1]
    return ''.join(filter(lambda ws: str.isalpha(ws) or str.isnumeric(ws) or ws == '_', item_name.replace('-', '_'))).lower()


  def add_waypoints(self):
    self.lines.append("WAYPOINT_TABLE = {")
    for item, data in self.logic_manager.waypoints.items():
      self.append_item(item, data, True)
    self.lines.append("}")


  def print_lua(self):
    self.lines = []
    self.set_header()
    self.add_space()
    self.add_locations()
    self.add_space()
    self.add_waypoints()
    with open(self.destination, 'w') as lua:
      for line in self.lines:
        lua.write(line)
        lua.write('\n')