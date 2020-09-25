from collections import defaultdict

class EnumerateWaypointPaths:

  '''
  EnumerateWaypointPaths takes a base location and its children, and determines
  all possible paths to each additional_children.

  This was used to determine how feasible it would be to automatically generate
  pathing based on the built-in waypoint system in the randomizer itself.

  The answer was 'not in any way'.
  '''

  def __init__(self, target, all_waypoints=[]):
    self.target = target
    self.all_waypoints = all_waypoints
    print(len(all_waypoints))
    self.waypoint_paths = {}


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
