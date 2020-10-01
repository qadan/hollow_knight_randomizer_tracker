----
-- Adds an item to the global progression bitmask.
--
-- mask (int): The mask to add as currently accessible.
-- group (int): The mask group the given mask belongs to.
----
function add_mask_to_group(mask, group)
  local new = PROGRESSION_BITMASK[group] | mask
  PROGRESSION_BITMASK[group] = new
end

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
-- Helper to add a counted, additive item set to the progression bitmask.
--
-- Used to track items like simple keys and dreamers where the specific item
-- picked up is not as important as the number of them the player has.
--
-- code (string): The tracker code defining this additive set.
-- additives (table<string>): A table containing the names of each additive in
-- the item set.
----
function add_additive_set(code, additives)
  local count = Tracker:ProviderCountForCode(code)
  for idx, item in ipairs(additives) do
    if count > idx - 1 then
      add_mask_to_group(ITEM_TABLE[item]['bitmask'], ITEM_TABLE[item]['group'])
    end
  end
end

----
-- Adds the current simple keys to the progression bitmask.
----
function add_simple_keys_to_bitmask()
  local keys = {
    'simple_key_sly',
    'simple_key_basin',
    'simple_key_city',
    'simple_key_lurker',
  }
  add_additive_set('simple_key', keys)
end

----
-- Adds the current dreamers to the progression bitmask.
----
function add_dreamers_to_bitmask()
  local dreamers = {
    'herrah',
    'monomon',
    'lurien',
    'dreamer',
  }
  add_additive_set('dreamers', dreamers)
end

----
-- Adds the 'CURSED' flag if NOTCURSED is off.
--
-- Kind of stupid in my opinion, but the source logic includes a flag for both
-- CURSED and NOTCURSED, so gotta handle.
----
function add_cursed_to_bitmask()
  local notcursed = Tracker:ProviderCountForCode('notcursed')
  if notcursed > 0 then
    add_mask_to_group(ITEM_TABLE['cursed']['bitmask'], ITEM_TABLE['cursed']['group'])
  end
end

----
-- Adds all currently-accessible waypoints to the progression bitmask.
----
function add_waypoints_to_bitmask()
  for waypoint, status in pairs(WAYPOINT_TABLE) do
    local count = Tracker:ProviderCountForCode(waypoint)
    if count > 0 then
      WAYPOINT_TABLE[waypoint]['status'] = true
      add_mask_to_group(status['bitmask'], status['group'])
    end
  end
  -- The for loop here is a total hack. We're basically just brute forcing our
  -- way through the waypoint tree, checking continued access to each node.
  -- @TODO: this number could be further optimized
  for i = 1, 15 do
    for waypoint, status in pairs(WAYPOINT_TABLE) do
      if status['status'] == false and can_get(status['postfix']) then
        WAYPOINT_TABLE[waypoint]['status'] = true
        add_mask_to_group(status['bitmask'], status['group'])
      end
    end
  end
end

----
-- Helper to recalculate access if necessary.
----
function recalculate_access()
  if SHOULD_CALCULATE then
    add_items_to_bitmask()
    add_simple_keys_to_bitmask()
    add_dreamers_to_bitmask()
    add_cursed_to_bitmask()
    add_waypoints_to_bitmask()
    SHOULD_CALCULATE = false
  end
end

----
-- Implementation of tracker_on_accessibility_updated().
--
-- Zeroes out the PROGRESSION_BITMASK and flags that it should be recalculated
-- at the first opportunity. Before access to any item or waypoint is
-- calculated, all current items are bitwise or'd into PROGRESSION_BITMASK, and
-- then accessible waypoints are bitwise or'd into PROGRESSION_BITMASK multiple
-- times to recurse through the entire waypoint graph until we're sure we've
-- calculated a fully valid set of waypoint access.
----
function tracker_on_accessibility_updated()
  PROGRESSION_BITMASK = {0, 0, 0, 0, 0, 0, 0}
  for waypoint, status in pairs(WAYPOINT_TABLE) do
    WAYPOINT_TABLE[waypoint]['status'] = false
  end
  SHOULD_CALCULATE = true
end