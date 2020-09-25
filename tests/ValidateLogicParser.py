from logic_utils.NestedParentheticals import NestedParentheticals

class ValidateLogicParser:

  TEST_STRING = '(A | B) + (C | (D | E)) + F + (G | H | (I + (J + K)))'
  AS_TREE = {
    'operator': '+',
    'statements': [
      {
        'operator': '|',
        'statements': ['A', 'B'],
      },
      {
        'operator': '|',
        'statements': [
          'C',
          {
            'operator': '|',
            'statements': ['D', 'E'],
          },
        ],
      },
      'F',
      {
        'operator': '|',
        'statements': [
          'G',
          'H',
          {
            'operator': '+',
            'statements': [
              'I',
              {
                'operator': '+',
                'statements': ['J', 'K'],
              },
            ],
          },
        ],
      },
    ],
  }

  def __init__(self):
    self.np = NestedParentheticals(self.TEST_STRING)


  def validate_logic_parser(self):
    assert len(self.np.statements) == 4, "Expected 4 statements, found {}".format(len(self.np.statements))
    assert self.np.operator == self.np.AND, "Top-level operator should be +, found {}".format(self.np.operator)
    assert self.np.to_tree() == self.AS_TREE, "Statements cast to tree mismatch expectations"