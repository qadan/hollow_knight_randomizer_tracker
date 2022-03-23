# Hollow Knight Randomizer Tracker Generation Tools

Tools to generate the Hollow Knight Randomizer Tracker for Emotracker.

Not really intended to be used by anyone, honestly; this is simply used to
generate the actual tracker that's submitted to Emotracker. Clone it if you'd
like, I'm not your dad

## Installation

Go to the [releases page](https://github.com/qadan/hkr_3_fantallis/releases/latest) and grab that. Or (ideally) download via emotracker?

This needs to run:

* ImageMagick `convert` should be in `PATH` to handle all the lovely pictures
* Python 3.8, maybe less, definitely not 2.7, don't do that

Some python packages like:

* Pillow
* JSON
* YAML
* math, i dunno, just keep running the root script and pip install until things stop exploding, i already have a venv set up so i'm not making an install manager

## Usage

Probably don't?

## What the hecko is in the resource foldero

* `images`: image folders for the resultant tracker. Mostly stuff that isn't dynamically generated and just needs some light processing.
* `locations`: .yaml files that define all of the different location types. No you may not have a schema.
* `rules`: .yaml files that are basically like the locations .yaml files but I felt icky leaving them in there because technically they are not like items
that you find in the world although the waypoints are also in the locations so like in the end nothing means anything and files go wherever you truly believe they belong<sub>1</sub>. I hope we've all learned something important here
*  `static_json`: These just get copied over to the base folder in the resultant tracker.
* `static_lua`: These just get copied over to the `scripts` folder in the resultant tracker.
* `base_folder_stuff`: Gets copied into the base folder.

<sup>1</sup>Note: files do not go wherever you truly believe they belong (@see Java). Keep your stuff organized.

## License

I put this under the GPL v3 license as if that's like going to be important for
any reason.
