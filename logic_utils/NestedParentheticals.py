class NestedParentheticals:

  '''
  HEREIN LIE MYSTERIOUS STRING SHENANIGANS TO UPSET ALL WHO GAZE THEREUPON

  This was originally used to determine if there was a way to use EmoTracker
  style interpretation of logic instead of postfix interpretation. It was dumped
  in favour of the latter.
  '''

  OPEN_BRACE = '('
  CLOSE_BRACE = ')'
  AND = '+'
  OR = '|'

  def __init__(self, string):
    self.string = string
    self.operator = self.get_first_operator()
    self.statements = self.get_statements()


  def get_first_operator(self):
    # Each nested parenthetical level only uses one type of operator.
    ignore_operators = False
    open_parenth = []
    for idx, char in enumerate(self.string):
      if char == self.OPEN_BRACE:
        ignore_operators = True
        open_parenth.append(idx)
      elif char == self.CLOSE_BRACE:
        open_parenth.pop()
        if not open_parenth:
          ignore_operators = False
      elif char == self.AND and not ignore_operators:
        return self.AND
      elif char == self.OR and not ignore_operators:
        return self.OR
    # In such a case, there are no operators at this level (we've reached
    # maximum recursive depth).
    return None


  def get_matching_close(self, start):
    open_parenth = []
    for idx, char in enumerate(self.string[start:]):
      if char == self.OPEN_BRACE:
        open_parenth.append(idx)
      elif char == self.CLOSE_BRACE:
        open_parenth.pop()
        if not open_parenth:
          return start + idx


  def get_statements(self):
    statements = []
    current_statement = ''
    idx = 0
    while idx < len(self.string):
      if self.string[idx] == self.OPEN_BRACE:
        if len(current_statement[:-3]):
          statements.append(current_statement[:-3].strip())
        close = self.get_matching_close(idx)
        statements.append(NestedParentheticals(self.string[idx+1:close]))
        current_statement = ''
        idx = close + 3
      elif self.string[idx] in [self.AND, self.OR] and len(current_statement[:-1]):
        statements.append(current_statement[:-1].strip())
        current_statement = ''
      else:
        current_statement += self.string[idx]
      idx += 1
    if len(current_statement):
      statements.append(current_statement.strip())
    return statements


  def to_tree(self):
    tree = {
      'operator': self.operator,
      'statements': [],
    }
    for statement in self.statements:
      if isinstance(statement, NestedParentheticals):
        tree['statements'].append(statement.to_tree())
      else:
        tree['statements'].append(statement)
    return tree
