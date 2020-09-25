----
-- Adds all current single-code tracked item codes to the progression bitmask.
----
function add_items_to_bitmask()
  for item, mask in pairs(ITEM_TABLE) do
    local count = Tracker:ProviderCountForCode(item)
    if count > 0 then
      add_mask_to_group(mask['bitmask'], mask['group'])
    end
  end
end

----
-- Adds the current simple keys to the progression bitmask.
--
-- A bit of a hack; it doesn't really matter which keys we're adding but rather
-- the count, so 'which one it is' doesn't reeeeeally have to map back to which
-- one was picked up. This way we can just generate the logic procedurally for
-- keys from the randomizer without having to mess with it.
----
function add_simple_keys_to_bitmask()
  local count = Tracker:ProviderCountForCode('simple_key')
  if count > 0 then
    add_mask_to_group(ITEM_TABLE['simple_key_sly']['bitmask'], ITEM_TABLE['simple_key_sly']['group'])
  end
  if count > 1 then
    add_mask_to_group(ITEM_TABLE['simple_key_basin']['bitmask'], ITEM_TABLE['simple_key_basin']['group'])
  end
  if count > 2 then
    add_mask_to_group(ITEM_TABLE['simple_key_city']['bitmask'], ITEM_TABLE['simple_key_city']['group'])
  end
  if count > 3 then
    add_mask_to_group(ITEM_TABLE['simple_key_lurker']['bitmask'], ITEM_TABLE['simple_key_lurker']['group'])
  end
end

----
-- Adds all currently-accessible waypoints to the progression bitmask.
----
function add_waypoints_to_bitmask()
  for waypoint, status in pairs(WAYPOINT_TABLE) do
    local count = Tracker:ProviderCountForCode(waypoint)
    if count > 0 then
      add_mask_to_group(WAYPOINT_TABLE[waypoint]['bitmask'], WAYPOINT_TABLE[waypoint]['group'])
    end
  end
  -- The for loop here is a total hack. We're basically just brute forcing our
  -- way through the waypoint tree, checking continued access to each node.
  -- @TODO: we could refine this number; 80 guarantees a path through the tree,
  -- but with some introspection it could be reduced or made dependent on your
  -- starting location.
  for i = 1, 80 do
    for waypoint, status in pairs(WAYPOINT_TABLE) do
      if can_get(WAYPOINT_TABLE[waypoint]['postfix']) then
        add_mask_to_group(WAYPOINT_TABLE[waypoint]['bitmask'], WAYPOINT_TABLE[waypoint]['group'])
      end
    end
  end
end

----
-- Implementation of tracker_on_accessibility_updated().
----
function tracker_on_accessibility_updated()
  PROGRESSION_BITMASK = {0, 0, 0, 0, 0, 0, 0}
  SHOULD_CALCULATE = true
end