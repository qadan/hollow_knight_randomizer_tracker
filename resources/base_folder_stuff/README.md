# Hollow Knight Randomizer 3 Tracker

## Introduction

A tracker for Hollow Knight Randomizer 3, configurable to use any combination of randomizer settings, and including all items able to be randomized.

The tracker is procedurally generated using the actual Hollow Knight Randomizer location definitions itself; see scripts/bitmasks.lua for more details.

## Installation

Either paste the .zip file in the [releases page](https://github.com/qadan/hollow_knight_randomizer_tracker/releases) into your EmoTracker's 'packs' folder and open it from inside EmoTracker, or (ideally) install through EmoTracker package management.

## Usage

### Starting location

The starting location is configurable by clicking the gear icon at the top right of the item tracker; the first pane that comes up is the start location. Clicking on it will cycle through different starting locations.

The icon is currently terrible; see the 'TODO' section.

### Randomization pools

By default, all randomization pools are turned on, which is probably not desireable. To change this, click the gear icon at the top right of the item tracker, then 'Pools'. This is the list of possible randomization pools that are turned on, and each of them can be right-clicked to turn them off, just like any other item.

Note that turning off randomization pools doesn't remove the items from the map - they're simply rendered inaccessible. This behaviour may change in the future; see the 'TODO' section.

Note as well that locations like Sly's shop always show the maximum amount of items you can get at that location. See the 'TODO' section as well.

### Skips

By default, no skips are taken into consideration, and cursed mode is turned off. To change this, click the gear icon at the top right of the item tracker, and then on the "Skips/Cursed" pane. From there, you can enable different skips.

The icons are currently terrible; see the 'TODO' section.

### Windowed Fullscreen

Running Hollow Knight in windowed fullscreen ensures that when you click the tracker outside the window, the window isn't minimized or otherwise hidden.

To do this in Steam:

* Right-click on "Hollow Knight" in your library
* Left-click on "Properties..."
* Under the "GENERAL" tab, click "SET LAUNCH OPTIONS..."
* In the window that pops up, type in "-screen-fullscreen 0 -popupwindow" (without the double quotes)
* Click "OK" to save your changes, then close the Properties window
* Launch the game, and it should be in windowed fullscreen.

## TODO

* Some of the map spots are too close together; they should either be moved, or reduced into 'part_of' grouped locations.
* The text-rendered icons are all terrible and need some work. They're generated through imagemagick, and that's fine, but the commands could be seriously improved, or could just make better icons.
* Some of the icons could be reduced; for example, the lifeblood requirements and dreamers and maybe some of the charms.
* If there's a way to do so (probably), it would be good to make it so disabling pools completely removes items from the map.
* Currently, the tracker is doing the maximum possible number of passes on waypoints to ensure locations are added to the logic; this has an associated click lag (as it's recalculating waypoint access 80 times per click), and it would be useful to calculate the maximum possible waypoint chain to reduce this number.
* 'Grouped' locations, if possible, should only show the number of actually accessible items through config.
* Round of testing.

## License

[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)