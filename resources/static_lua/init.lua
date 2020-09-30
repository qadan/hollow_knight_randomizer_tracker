Tracker:AddItems("items/start_locations.json")
Tracker:AddItems("items/options.json")
Tracker:AddItems("items/skips.json")
Tracker:AddItems("items/items.json")

if not (string.find(Tracker.ActiveVariantUID, "items_only")) then
  Tracker:AddMaps("maps/map.json")
  ScriptHost:LoadScript("scripts/bitmasks.lua")
  ScriptHost:LoadScript("scripts/progression_interpreter.lua")
  ScriptHost:LoadScript("scripts/update.lua")
  tracker_on_accessibility_updated()
  Tracker:AddLocations("locations/locations.json")
end

Tracker:AddLayouts("layouts/item_grids.json")
Tracker:AddLayouts("layouts/tracker.json")
Tracker:AddLayouts("layouts/broadcast.json")