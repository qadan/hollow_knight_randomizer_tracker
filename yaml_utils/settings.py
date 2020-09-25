from yaml import safe_load

'''
Helpers to mess with the settings yaml.
'''

def get_settings():
  with open('settings.yaml', 'r') as settings:
    return safe_load(settings)


def get_setting(setting):
  settings = get_settings()
  try:
    return settings['settings'][setting]
  except IndexError:
    return None


def get_mod_path():
  return get_setting('mod_path')
