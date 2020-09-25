#!/usr/bin/python3.8

from tests.ValidateLocationYaml import ValidateLocationYaml
from tests.ValidateLogicParser import ValidateLogicParser

def run_them_tests():
  validator = ValidateLocationYaml()
  validator.validate_location_yaml()
  logic_tester = ValidateLogicParser()
  logic_tester.validate_logic_parser()


if __name__ == '__main__':
  try:
    run_them_tests()
    print('No tests failed.')
  except AssertionError as fail:
    print(fail)