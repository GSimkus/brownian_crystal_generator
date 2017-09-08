#About:
A diffusion-limited agglomeration script written in python.

Uses MatPlotLib to render a board of particles "points", which are stored as sets of tuples of coordinates (rather than storing a (sparse) matrix).

During the run, each new addition to the agglomeration "glom" is logged in a csv in /data/<start time in %Y.%m.%d.%H.%M" format>, and stills of the process are captured as according to the "frames to snag" setting used in parameters.py

The neighbors function lists the cells considered adjacent to a particle, and thus dictates the movement properties of a particle.
