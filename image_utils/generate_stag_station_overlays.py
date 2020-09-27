from yaml_utils.LocationYaml import LocationYaml
from image_utils.TextGeneratedImage import TextGeneratedImage

def get_letter_pair(station):
  # Display names take the format 'PLACE NAME Station'. No place names are
  # longer than two words, so either take the first letter of the two words,
  # or the first two letters of the only word. Fortunately there's no overlap
  # ... FOR NOW dun dun dunnnn
  bits = station.split(' ')
  if len(bits) == 3:
    return '{}{}'.format(bits[0][:1], bits[1][:1])
  else:
    return bits[0][:2]


def get_overlay_params(text):
  return '-background transparent -size 32x32 -pointsize 15 -gravity southeast -fill white label:\'{}\''.format(text)


def get_full_destination(destination, station):
  return '{}/images/overlays/{}_overlay.png'.format(destination, station)

def generate_stag_station_overlays(destination):
  for station in LocationYaml().get_locations('stag_stations'):
    letter_pair = get_letter_pair(station['display_name'])
    station_overlay = TextGeneratedImage('', get_overlay_params(letter_pair))
    station_overlay.front = get_full_destination(destination, station['location_name'])
    station_overlay.generate_image()