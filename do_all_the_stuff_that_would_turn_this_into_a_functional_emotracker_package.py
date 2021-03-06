#!/usr/bin/python3.8

from argparse import ArgumentParser
from os import mkdir, walk, path
from shutil import copy2 # electric boogaloo
from glob import glob
from json import dump
from image_utils.ResourceIncludedImage import ResourceIncludedImage
from image_utils.generate_stag_station_overlays import generate_stag_station_overlays
from json_utils.GenerateItems import GenerateItems
from json_utils.GenerateBitmaskedLocations import GenerateBitmaskedLocations
from json_utils.GenerateOptions import GenerateOptions
from json_utils.GenerateSkips import GenerateSkips
from json_utils.GenerateStartLocations import GenerateStartLocations
from json_utils.GenerateCapturables import GenerateCapturables
from logic_utils.GenerateLogicLua import GenerateLogicLua
from yaml_utils.settings import get_setting
from zipfile import ZipFile, ZIP_DEFLATED

def get_the_args():
  parser = ArgumentParser(description='wow its gonna do some stuff')
  parser.add_argument('--out_folder', help='output folder. delete this first because do it', required=True)
  return vars(parser.parse_args())


def prep_a_folder(folder):
  print('Prepping a folder ...')
  # imagine not catching FileExistsError in 2020
  try:
    mkdir(folder)
  except FileExistsError:
    print('there is already a pack there genus')
    return
  pack_dir_structure = [
    'images',
    'images/items',
    'images/options',
    'images/maps',
    'images/overlays',
    'default',
    'scripts',
    'items',
    'layouts',
    'items_only',
    'items_only/layouts',
    'locations',
    'maps',
  ]
  for subfolder in pack_dir_structure:
    mkdir('{}/{}'.format(folder, subfolder))


def move_some_static_stuff_into_the_folder(folder):
  print('Copying some static stuff into the folder ...')
  to_move = {
    'images/maps/*.png': 'images/maps',
    'images/options/*.png': 'images/options',
    'images/overlays/*.png': 'images/overlays',
    'static_json/manifest.json': '.',
    'static_json/settings.json': '.',
    'static_json/maps/*.json': 'maps',
    'static_json/layouts/*.json': 'layouts',
    'static_json/items_only/*.json': 'items_only',
    'static_json/items_only/layouts/*.json': 'items_only/layouts',
    'static_lua/*.lua': 'scripts',
    'base_folder_stuff/*': '.',
  }
  for source, destination in to_move.items():
    for file in glob('resources/{}'.format(source)):
      copy2(file, '{}/{}'.format(folder, destination))


def move_and_format_the_images(folder):
  print('Copying and formatting images ...')
  destination = '{}/images/items'.format(folder)
  for file in glob('resources/images/items/*.png'):
    ResourceIncludedImage(file).copy_the_thing(destination)


def generate_location_json(folder):
  print('Generating location JSON ...')
  location_json = GenerateBitmaskedLocations()
  with open('{}/locations/locations.json'.format(folder), 'w') as fout:
    dump(location_json.get_locations(), fout, sort_keys=get_setting('sort_json_keys'), indent=get_setting('json_indent'))



def generate_options_json(folder):
  print('Generating options JSON ...')
  opts_json = GenerateOptions(folder)
  opts_json.flatten_images()
  with open('{}/items/options.json'.format(folder), 'w') as fout:
    dump(opts_json.get_options(), fout, sort_keys=get_setting('sort_json_keys'), indent=get_setting('json_indent'))


def generate_skips_json(folder):
  print('Generating skips JSON ...')
  skips_json = GenerateSkips(folder)
  skips_json.flatten_images()
  with open('{}/items/skips.json'.format(folder), 'w') as fout:
    dump(skips_json.get_skips(), fout, sort_keys=get_setting('sort_json_keys'), indent=get_setting('json_indent'))


def generate_start_locations_json(folder):
  print('Generating start location JSON ...')
  start_json = GenerateStartLocations()
  start_json.generate_images(folder)
  start_json.flatten_images()
  with open('{}/items/start_locations.json'.format(folder), 'w') as fout:
    dump(start_json.get_start_locations(), fout, sort_keys=get_setting('sort_json_keys'), indent=get_setting('json_indent'))


def generate_items_json(folder):
  print('Generating items JSON ...')
  item_json = GenerateItems()
  with open('{}/items/items.json'.format(folder), 'w') as fout:
    dump(item_json.generate_items(), fout, sort_keys=get_setting('sort_json_keys'), indent=get_setting('json_indent'))


def generate_capturables_json(folder):
  print('Generating capturables JSON ...')
  cap_json = GenerateCapturables()
  with open('{}/items/capturables.json'.format(folder), 'w') as fout:
    dump(cap_json.get_capturables(), fout, sort_keys=get_setting('sort_json_keys'), indent=get_setting('json_indent'))


def generate_bitmask_lua(folder):
  print('Generating bitmask Lua ...')
  logic = GenerateLogicLua('{}/scripts/bitmasks.lua'.format(folder))
  logic.print_lua()


if __name__ == '__main__':
  args = get_the_args()
  prep_a_folder(args['out_folder'])
  move_some_static_stuff_into_the_folder(args['out_folder'])
  move_and_format_the_images(args['out_folder'])
  generate_location_json(args['out_folder'])
  generate_options_json(args['out_folder'])
  generate_skips_json(args['out_folder'])
  generate_start_locations_json(args['out_folder'])
  generate_items_json(args['out_folder'])
  generate_capturables_json(args['out_folder'])
  generate_stag_station_overlays(args['out_folder'])
  generate_bitmask_lua(args['out_folder'])