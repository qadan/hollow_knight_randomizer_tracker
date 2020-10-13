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

## @TODO for 1.2.0 and beyond

* The map is pretty gosh darn big; we could have a variant that's split by region.

## License

[GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)
