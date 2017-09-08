# About:
A diffusion-limited aggregate script written in python as a personal project in complexity science. In addition to the serious applications in complexity and systems science it's good for making funky "brownian crystals" (aka DLA clusters) and also by using the "animate" toggle in the parameters you can watch the dots move in real time (actually significantly less quickly than not animating).

Uses MatPlotLib to render a board of particles "`points`", which are stored as sets of tuples of coordinates (rather than storing a (sparse) matrix).

During the run, each new addition to the aggregate/agglomeration or "`glom`" is logged in a csv in `/data/<start time in %Y.%m.%d.%H.%M" format>`, and stills of the process are captured as according to the "`frames to snag`" setting used in parameters.py

The neighbors function lists the cells considered adjacent to a particle, and thus dictates the movement properties of a particle.


## Fun settings
"snow"
- animate set to True (or 1)
- `cmap = colors.ListedColormap([[0,0,0.2], [1,1,1], [0.7,0.9,1]])`
- disallow any "y-1"s from neighbours (or add additional y+1s)
- starting glom as "`bottom`" or "`{(bounds[0]-1,i) for i in range(bounds[1])}`"
- spawnsquares as "`top`" or "`{(0,i) for i in range(bounds[1])}`"
- the `bounds`, `simpoints`, point spawning logic, and `dot_sidelength_in_pixels` as whatever looks nice and runs well on your rig
