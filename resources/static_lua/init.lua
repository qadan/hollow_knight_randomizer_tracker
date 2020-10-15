-- Base item set.
Tracker:AddItems("items/items.json")

-- Considerations for map trackers. Only one exists currently, but leaving open
-- to add more in the future.
if not (string.find(Tracker.ActiveVariantUID, "items_only")) then

  -- Configuration "items" to flag the player start location.
  Tracker:AddItems("items/start_locations.json")
  -- Configuration "items" to flag which things are randomized.
  Tracker:AddItems("items/options.json")
  -- Configuration "items" to flag which skips are enabled.
  Tracker:AddItems("items/skips.json")
  -- Items which don't matter for progression but which the player may want to
  -- track on the map.
  Tracker:AddItems("items/capturables.json")

  Tracker:AddMaps("maps/complete_map.json")

  ScriptHost:LoadScript("scripts/bitmasks.lua")
  ScriptHost:LoadScript("scripts/progression_interpreter.lua")
  ScriptHost:LoadScript("scripts/update.lua")

  -- Generate and reset global variables.
  tracker_on_accessibility_updated()

  -- Now that everything is loaded, do the first accessibility pass.
  Tracker:AddLocations("locations/locations.json")

end

-- Tracker grids and broadcast view.
Tracker:AddLayouts("layouts/item_grids.json")
Tracker:AddLayouts("layouts/tracker.json")
Tracker:AddLayouts("layouts/broadcast.json")