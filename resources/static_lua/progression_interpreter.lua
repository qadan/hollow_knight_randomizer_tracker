----
-- Helper function to reference in location json; referenced in access_rules.
--
-- If this is the first item being evaluated on this logical pass, the current
-- progression bitmask is calculated at this time.
--
-- item_name (string): The name of the item to look up.
----
function can_get_item(item_name)
  recalculate_access()
  return can_get(ITEM_TABLE[item_name]['postfix'], PROGRESSION_BITMASK)
end

----
-- Helper function to reference in location json; checks using skip bitmask.
--
-- item_name (string): The name of the item to look up.
----
function can_skip_to_item(item_name)
  recalculate_access()
  return can_get(ITEM_TABLE[item_name]['postfix'], SKIP_BITMASK)
end

----
-- Helper function to determine access to a waypoint.
--
-- waypoint (string): The waypoint to determine access to.
----
function can_get_waypoint(waypoint)
  local count = Tracker:ProviderCountForCode(waypoint)
  if count > 0 then
    return count
  end
  recalculate_access()
  return can_get(WAYPOINT_TABLE[waypoint]['postfix'], PROGRESSION_BITMASK)
end

----
-- Helper function to determine checkability of an item.
--
-- item (string): The item to determine checkability of.
----
function can_check_item(item_name)
  recalculate_access()
  return can_get(CHECK_TABLE[item_name], PROGRESSION_BITMASK)
end

----
-- Helper function to determine checkability of an item with skips.
--
-- item (string): The item to determine checkability of.
----
function can_skip_to_check_item(item_name)
  recalculate_access()
  return can_get(CHECK_TABLE[item_name], SKIP_BITMASK)
end

----
-- Determines the accessibility of something by interpreting its postfix table.
--
-- After processing the postfix table against its postfixed operators, we
-- should be left with a single boolean value we can return as accessibility.
--
-- logic (table<int, int>): a table comparing the mask for an item or waypoint
--   with the group it comes from. No masks should be 0. Masks less than 1
--   represent special data or operators.
----
function can_get(logic, progression_bitmask)
  if next(logic) == nil then
    return true
  end

  local stack = {}
  for _,postfix in ipairs(logic) do
    -- Comparing two conditions using ADD.
    if postfix[1] == -2 then
      local comp_1 = table.remove(stack)
      local comp_2 = table.remove(stack)
      table.insert(stack, comp_1 and comp_2)
    -- Comparing two conditions using OR.
    elseif postfix[1] == -1 then
      local comp_1 = table.remove(stack)
      local comp_2 = table.remove(stack)
      table.insert(stack, comp_1 or comp_2)
    -- We don't check conditions less than -2 in the tracker; these represent
    -- requisite grub and essence counts, which are generated randomly and
    -- cannot be tracked without access to the game state. Instead, consider
    -- these 'true' and show them as orange locations (TODO WINKY FACE).
    elseif postfix[1] < -2 then
      table.insert(stack, true)
    else
      table.insert(stack, postfix[1] & progression_bitmask[postfix[2]] == postfix[1])
    end
  end
  return table.remove(stack)
end