----
-- Adds an item to a progression bitmask.
--
-- bitmask (table<int>): The bitmask to add a value to.
-- mask (int): The mask to add as currently accessible.
-- group (int): The mask group the given mask belongs to.
--
-- Returns the updated bitmask.
----
function add_mask_to_group(bitmask, mask, group)
  bitmask[group] = bitmask[group] | mask
  return bitmask

end

----
-- Adds all toggleable progression item codes to the given bitmask table.
--
-- bitmask (table<int>): The bitmask table to add items to.
----
function add_items_to_bitmask(bitmask)
  for item, mask in pairs(ITEM_TABLE) do
    -- Non-progression items won't have bitmasks.
    if mask['bitmask'] ~= nil then
      local count = Tracker:ProviderCountForCode(item)
      if count > 0 then
        bitmask = add_mask_to_group(bitmask, mask['bitmask'], mask['group'])
      end
    end
  end
  return bitmask
end

----
-- Helper to add a counted, additive item set to the progression bitmask.
--
-- Used to track items like simple keys and dreamers where the specific item
-- picked up is not as important as the number of them the player has.
--
-- bitmask (table<int>): The bitmask table to add the set to.
-- code (string): The tracker code defining this additive set.
-- additives (table<string>): A table containing the names of each additive in
-- the item set.
----
function add_additive_set(bitmask, code, additives)
  local count = Tracker:ProviderCountForCode(code)
  for idx, item in ipairs(additives) do
    if count > idx - 1 then
      bitmask = add_mask_to_group(bitmask, ITEM_TABLE[item]['bitmask'], ITEM_TABLE[item]['group'])
    end
  end
  return bitmask
end

----
-- Adds the current simple keys to the progression bitmask.
--
-- bitmask (table<int>): The bitmask table to add simple keys to.
----
function add_simple_keys_to_bitmask(bitmask)
  local keys = {
    'simple_key_sly',
    'simple_key_basin',
    'simple_key_city',
    'simple_key_lurker',
  }
  return add_additive_set(bitmask, 'simple_key', keys)
end

----
-- Adds the current dreamers to the progression bitmask.
--
-- bitmask (table<int>): The bitmask table to add dreamers to.
----
function add_dreamers_to_bitmask(bitmask)
  local dreamers = {
    'herrah',
    'monomon',
    'lurien',
    'dreamer',
  }
  return add_additive_set(bitmask, 'dreamers', dreamers)
end

----
-- Adds the 'CURSED' flag if NOTCURSED is off.
--
-- Kind of stupid in my opinion, but the source logic includes a flag for both
-- CURSED and NOTCURSED, so gotta handle.
--
-- bitmask (table<int>): The bitmask table to add the cursed status to.
-- level (string): The level that 'notcursed' should be at to add the flag - one of
-- 'red', 'yellow', or 'green'.
----
function add_cursed_to_bitmask(bitmask, level)
  local notcursed = Tracker:ProviderCountForCode('notcursed_' .. level)
  if notcursed == level then
    return add_mask_to_group(bitmask, SKIP_TABLE['cursed']['bitmask'], SKIP_TABLE['cursed']['group'])
  end
  return bitmask
end

----
-- Adds all skips to the given bitmask.
--
-- bitmask (table<int>): The bitmask table to add skips to.
-- level (string): The level the skips should be at to add the flag - one of
-- 'red', 'yellow', or 'green'.
----
function add_skips_to_bitmask(bitmask, level)
  for skip, data in pairs(SKIP_TABLE) do
    local count = Tracker:ProviderCountForCode(skip .. '_' .. level)
    if count > 0 then
      bitmask = add_mask_to_group(bitmask, data['bitmask'], data['group'])
    end
  end
  return bitmask
end

----
-- Adds all currently-accessible waypoints to the progression bitmask.
--
-- bitmask (table<int>): The bitmask table to add waypoints to.
----
function add_waypoints_to_bitmask(bitmask)
  for waypoint, status in pairs(WAYPOINT_TABLE) do
    local count = Tracker:ProviderCountForCode(waypoint)
    if count > 0 then
      bitmask = add_mask_to_group(bitmask, status['bitmask'], status['group'])
    end
  end
  -- Traverse the waypoint tree. If we make a pass and no new waypoints are
  -- accessible, we can stop.
  local pass_again = true
  while pass_again do
    pass_again = false
    for waypoint, status in pairs(WAYPOINT_TABLE) do
      if status['bitmask'] & bitmask[status['group']] ~= status['bitmask'] and can_get(status['postfix'], bitmask) then
        pass_again = true
        bitmask = add_mask_to_group(bitmask, status['bitmask'], status['group'])
      end
    end
  end
  return bitmask
end

----
-- Helper to recalculate access if necessary.
----
function recalculate_access()
  if SHOULD_CALCULATE then
    PROGRESSION_BITMASK = add_items_to_bitmask(PROGRESSION_BITMASK)
    PROGRESSION_BITMASK = add_simple_keys_to_bitmask(PROGRESSION_BITMASK)
    PROGRESSION_BITMASK = add_dreamers_to_bitmask(PROGRESSION_BITMASK)
    PROGRESSION_BITMASK = add_skips_to_bitmask(PROGRESSION_BITMASK, 'green')
    PROGRESSION_BITMASK = add_cursed_to_bitmask(PROGRESSION_BITMASK, 'green')
    for idx, value in ipairs(PROGRESSION_BITMASK) do
      SKIP_BITMASK[idx] = value
    end
    PROGRESSION_BITMASK = add_waypoints_to_bitmask(PROGRESSION_BITMASK)
    SKIP_BITMASK = add_skips_to_bitmask(SKIP_BITMASK, 'yellow')
    SKIP_BITMASK = add_cursed_to_bitmask(SKIP_BITMASK, 'yellow')
    SKIP_BITMASK = add_waypoints_to_bitmask(SKIP_BITMASK)
    SHOULD_CALCULATE = false
  end
end

----
-- Implementation of tracker_on_accessibility_updated().
--
-- Resets the following global variables:
--   PROGRESSION_BITMASK (table<int>): Seven 32-bit integers representing the
--   player's current clear access.
--   SKIP_BITMASK (table<int>): Seven 32-bit integers representing what the
--   player would have access to via currently-yellow skips.
--   SHOULD_CALCULATE (bool): Whether or not to recalculate all access when
--   checking a new location.
----
function tracker_on_accessibility_updated()
  PROGRESSION_BITMASK = {0, 0, 0, 0, 0, 0, 0}
  SKIP_BITMASK = {0, 0, 0, 0, 0, 0, 0}
  SHOULD_CALCULATE = true
end