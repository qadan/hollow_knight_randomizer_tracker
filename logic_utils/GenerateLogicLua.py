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

  def __init__(self, destination):
    self.logic_manager = LogicManager()
    self.logic_manager.parse_xml()
    self.lines = []
    self.destination = destination


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


  def set_table_doc(self):
    self.lines.extend([
      '----',
      '-- ITEM_TABLE and WAYPOINT_TABLE:',
      '--   Tables containing information to be used to determine the accessibility of',
      '--   items and waypoints, respectively, using item or waypoint names as keys,',
      '--   paired with the following values:',
      '--   - \'bitmask\': (Optional) A power of two; the bit representing this item or',
      '--     waypoint in the PROGRESSION_BITMASK in its group. If absent, this item',
      '--     does not provide progression.',
      '--   - \'group\': (Optional) A number between 1 and 7; the group in the',
      '--     PROGRESSION_BITMASK this item or waypoint is represented in. If absent,',
      '--     this item does not provide progression.',
      '--   - \'postfix\': A list of postfixed, processed logic representing access to',
      '--     this item or waypoint. Each item is a bitmask/group pair representing',
      '--     where to look in the PROGRESSION_BITMASK for access. Negative integers',
      '--     represent operators; -2 is AND, and -1 is OR. Lower numbers are not',
      '--     considered currently.',
      '--   - \'status\': Currently unused, but should be used in the future to',
      '--     optimize waypoint logic check passes.',
      '--',
      '-- For example, in \'lurien\' in the ITEM_TABLE, the first 5 postfixes match the',
      '-- bitmask and bitmask groups of the \'right_city\' waypoint, the mantis_claw,',
      '-- and \'dreamnail\', which has been expanded to mean one of dream_nail,',
      '-- dream_gate, or awoken_dream_nail. The interpreter asks whether each of these',
      '-- have been obtained, and adds a \'true\' or \'false\' to the stack. After this',
      '-- the interpreter encounters a {-1, 1}, telling it to remove the top two things',
      '-- things on the stack (awoken_dream_nail and dream_gate), logically OR them',
      '-- together, and add the results of this comparison to the top of the stack.',
      '--',
      '-- Eventually, after adding to, removing from, and comparing things in the stack,',
      '-- only one value will be left - the definitive assertion of whether or not the',
      '-- item is accessible.',
      '----',
    ])


  def set_check_doc(self):
    self.lines.extend([
      '----',
      '-- CHECK_TABLE:',
      '--   Table containing mostly identical postfixes to the WAYPOINT and ITEM_TABLEs',
      '--   but pared down to display only the access necessary to check the location',
      '--   (e.g., being able to see a whispering root\'s prize without the Dreamnail).',
      '--',
      '--   Each item in the table is paired with the postfix list of accessibility',
      '--   rules defining whether the item is checkable.',
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


  def add_checks(self):
    self.lines.append("CHECK_TABLE = {")
    for item, data in self.logic_manager.items.items():
      if 'processedCheckLogic' in data:
        self.lines.append("  {} = {{".format(self.clean_name(item)))
        for postfix in data['processedCheckLogic']:
          self.lines.append("    {{{}, {}}},".format(postfix[0], postfix[1]))
        self.lines.append("  },")
    self.lines.append("}")



  def print_lua(self):
    self.lines = []
    self.set_header()
    self.add_space()
    self.set_table_doc()
    self.add_locations()
    self.add_space()
    self.add_waypoints()
    self.add_space()
    self.set_check_doc()
    self.add_checks()
    with open(self.destination, 'w') as lua:
      for line in self.lines:
        lua.write(line)
        lua.write('\n')