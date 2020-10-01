from collections import defaultdict
from pathlib import Path
from yaml import safe_load, parser

class EnumerateWaypointPaths:

  '''
  EnumerateWaypointPaths takes a base location and its children, and determines
  all possible paths to each additional_children.

  This was used to determine how feasible it would be to automatically generate
  pathing based on the built-in waypoint system in the randomizer itself.

  The answer was 'not in any way'.
  '''

  def __init__(self, target):
    self.target = target
    self.all_waypoints = {}
    self.get_waypoints()
    self.waypoint_paths = {}


  def get_waypoints(self):
    with open(Path('resources/locations/waypoints.yaml'), 'r') as waypoint_yaml:
      waypoints = safe_load(waypoint_yaml)
      for waypoint, data in waypoints['waypoints'].items():
        self.all_waypoints[waypoint] = [waypoint for waypoint in data['child_waypoints'].keys()]


  def get_paths_for(self, start_child):
    path = [start_child]
    seen = {start_child}
    def search_graph():
      if path[-1] not in self.all_waypoints:
        yield list(path)
      dead_end = True
      for waypoint in self.all_waypoints[path[-1]]:
        if waypoint not in seen:
          dead_end = False
          seen.add(waypoint)
          path.append(waypoint)
          yield from search_graph()
          path.pop()
          seen.remove(waypoint)
      if dead_end:
        yield list(path)
    yield from search_graph()


  def get_enumerated_waypoints(self):
    if not self.waypoint_paths:
        self.waypoint_paths = sorted(self.get_paths_for(self.target))
    return self.waypoint_paths


  def longest_waypoint_path(self):
    longest = (None, 0)
    for start, children in self.get_enumerated_waypoints().items():
      for child in children:
        if len(child) > longest[1]:
          longest = (start, child)
    return longest