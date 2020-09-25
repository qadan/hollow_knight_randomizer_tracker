from re import match, findall

class LogicShuntingYard:

  OPS = "+|()"
  COMPS = "+|"


  def __init__(self, infix, macros):
    self.infix = infix
    self.macros = macros
    self.pointer = 0


  def get_next_operator(self):
    start_char = self.pointer
    if self.infix[self.pointer] in self.OPS:
      self.pointer += 1
      return self.infix[self.pointer - 1]
    while self.pointer < len(self.infix) - 1 and self.infix[self.pointer] not in self.OPS:
      self.pointer += 1
    return self.infix[start_char:self.pointer].strip()


  def generate_postfix():
    self.pointer = 0
    stack = []
    postfix = []

    while self.pointer < len(self.infix) - 1:
      next_op = self.get_next_operator()
      if next_op.strip() == '':
        continue
      if next_op in self.COMPS:
        while not stack and (next_op in self.COMPS and stack[-1] != '|') and stack[-1] != '(':
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
