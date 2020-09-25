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
-- Helper function to reference in location json; referenced in access_rules.
--
-- If this is the first item being evaluated on this logical pass, the current
-- progression bitmask is calculated at this time.
--
-- item_name (string): The name of the item to look up.
----
function can_get_item(item_name)
  if SHOULD_CALCULATE then
    add_items_to_bitmask()
    add_simple_keys_to_bitmask()
    add_waypoints_to_bitmask()
    SHOULD_CALCULATE = false
  end
  return can_get(ITEM_TABLE[item_name]['postfix'])
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
  if SHOULD_CALCULATE then
    add_items_to_bitmask()
    add_simple_keys_to_bitmask()
    add_waypoints_to_bitmask()
    SHOULD_CALCULATE = false
  end
  return can_get(WAYPOINT_TABLE[waypoint]['postfix'])
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
function can_get(logic)
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
      table.insert(stack, postfix[1] & PROGRESSION_BITMASK[postfix[2]] == postfix[1])
    end
  end
  return table.remove(stack)
end

function can_get_debug(logic)
  -- Empty logic means it's simply accessible.
  if next(logic) == nil then
    return true
  end

  local stack = {}
  for _,postfix in ipairs(logic) do
    -- Comparing two conditions using ADD.
    if postfix[1] == -2 then
      local comp_1 = table.remove(stack)
      local comp_2 = table.remove(stack)
      if comp_1 and comp_2 then
        print("Comparison of " .. comp_1 .. " and " .. comp_2 .. " returned true")
      else
        print("Comparison of " .. comp_1 .. " and " .. comp_2 .. " returned false")
      end
      table.insert(stack, comp_1 and comp_2)
    -- Comparing two conditions using OR.
    elseif postfix[1] == -1 then
      local comp_1 = table.remove(stack)
      local comp_2 = table.remove(stack)
      if comp_1 or comp_2 then
        print("Comparison of " .. comp_1 .. " or " .. comp_2 .. " returned true")
      else
        print("Comparison of " .. comp_1 .. " or " .. comp_2 .. " returned false")
      end
      table.insert(stack, comp_1 or comp_2)
    -- We don't check conditions less than -2 in the tracker; these represent
    -- requisite grub and essence counts, which are generated randomly and
    -- cannot be tracked without access to the game state. Instead, consider
    -- these 'true' and show them as orange locations (TODO WINKY FACE).
    elseif postfix[1] < -2 then
      print("A condition of less than -2 was encountered, therefore we return true")
      table.insert(stack, true)
    else
      if postfix[1] & PROGRESSION_BITMASK[postfix[2]] == postfix[1] then
        print("Bitwise and comparison of " .. postfix[1] .. " and the bitmask " .. PROGRESSION_BITMASK[postfix[2]] .. " at bitmask position " .. postfix[2] .. " was equal to the initial input")
      else
        print("Bitwise and comparison of " .. postfix[1] .. " and the bitmask " .. PROGRESSION_BITMASK[postfix[2]] .. " at bitmask position " .. postfix[2] .. " was not equal to the initial input")
      end
      table.insert(stack, postfix[1] & PROGRESSION_BITMASK[postfix[2]] == postfix[1])
    end
  end
  local last_thing = table.remove(stack)
  if last_thing then
    print("The last item on the stack was true")
  else
    print("The last item on the stack was false")
  end
  return last_thing
end