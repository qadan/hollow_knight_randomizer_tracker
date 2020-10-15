----
-- Assert an item is accessible using PROGRESSION_BITMASK.
--
-- item_name (string): The name of the item to look up.
----
function can_get_item(item_name)
  recalculate_access()
  return can_get(ITEM_TABLE[item_name]['postfix'], PROGRESSION_BITMASK)
end

----
-- Assert an item is accessible using SKIP_BITMASK.
--
-- item_name (string): The name of the item to look up.
----
function can_skip_to_item(item_name)
  recalculate_access()
  return can_get(ITEM_TABLE[item_name]['postfix'], SKIP_BITMASK)
end

----
-- Assert a waypoint is accessible using PROGRESSION_BITMASK.
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
-- Assert an item is checkable without skips.
--
-- item (string): The item to determine checkability of.
----
function can_check_item(item_name)
  recalculate_access()
  return can_get(CHECK_TABLE[item_name], PROGRESSION_BITMASK)
end

----
-- Assert an item is checkable with skips.
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
-- After processing the postfix table, we should be left with a single boolean
-- value we can return as an assertion of accessibility.
--
-- logic (table<int, int>): a table of integer pairs. The second integer in each
-- pair is the index in progression_bitmask to check, and the first integer is a
-- power of two (up to 31 squared) representing the bit at that index to check.
-- The number 0 should not occur (though it would have no effect). Numbers less
-- than 0 represent special values or operators to be handled.
-- progression_bitmask (table<int>): The progression bitmask to check logical
-- access in.
----
function can_get(logic, progression_bitmask)
  if next(logic) == nil then
    return true
  end

  local stack = {}
  for _, postfix in ipairs(logic) do
    -- -2 flags a comparison using AND.
    if postfix[1] == -2 then
      local comp_1 = table.remove(stack)
      local comp_2 = table.remove(stack)
      table.insert(stack, comp_1 and comp_2)
    -- -1 flags a comparison using OR.
    elseif postfix[1] == -1 then
      local comp_1 = table.remove(stack)
      local comp_2 = table.remove(stack)
      table.insert(stack, comp_1 or comp_2)
    -- Conditions less than -2 represent grub and essence counts; these are not
    -- currently tracked.
    elseif postfix[1] < -2 then
      table.insert(stack, true)
    else
      table.insert(stack, postfix[1] & progression_bitmask[postfix[2]] == postfix[1])
    end
  end
  return table.remove(stack)
end