# About:
A diffusion-limited aggregate script where particles undergo a random walk until they collide with an aggregate whereupon they are added to the "agg".

![A typical crystal growth](https://i.imgflip.com/1wihh5.gif)

I wrote this in python as a personal project in particle simulation complexity science. In addition to the serious applications (models like this are used in simulation of chemical reactions, plant and coral growth, state changes in materials, biophysics, *etc.*) it's also good for making funky "brownian crystals" (aka "DLA clusters") - one can also use the `animate` toggle in `parameters.py` to watch the dots move in real time (note: since the time between frames is locked here, you will want to boost the number of simultaneously simulated particles (`simpoints`), which is both prettier to watch and also is set fairly low in the current parameters file, since using fewer points allows for many more frames to be run in the same time period especially on weaker hardware).

Uses MatPlotLib to render a board of `particles` or `parts`, which are stored as sets of tuples of coordinates (another option would be storing a (sparse) matrix and updating that, but it's not the method used here primarily because this is more tweakable)

During the run, each new addition to the `aggregate` or `agg` is logged in a csv in `/data/<start time in %Y.%m.%d.%H.%M format>`, and stills of the process are captured as according to the `frames to snag` setting used in config.ini (The next update will add a gui for selecting a directory and adding settings)

Note: When resuming a run (setting `continue_previous_run` to `true`, `1`, `yes`, or `on`), config.ini will load the config file from `prev_run`, and use those settings. Updating, renaming, or deleting that file causes the settings in the main directory's config.ini to be kept active.

Config.ini has a lot of annotation, so please read that for more information on settings.

## Fun settings
"snow"
![So Christmas-y](<insert image here>)
- animate set to `true`, `1`, `yes`, or `on`
- `cmap = colors.ListedColormap([[0,0,0.2], [1,1,1], [0.7,0.9,1]])`
- disallow any lines with `y-1` from `movement_options` (or add additional `y+1`s)
- `starting_agg` as `bottom` or "`{(bounds[0]-1,i) for i in range(bounds[1])}`"
- `spawnsquares` as "`top`" or "`{(0,i) for i in range(bounds[1])}`"
- the `bounds`, `simpoints`, point spawning logic, and `dot_sidelength_in_pixels` as whatever looks nice and runs well on your rig


## Dependencies
- Python 3
- numpy
- matplotlib
