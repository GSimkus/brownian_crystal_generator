from ast import literal_eval
from matplotlib import animation, rc, colors

# Constants and run parameters
continue_previous_run = False
prev_run = "2017.09.07.17.42"

if not continue_previous_run:
    startingglom = {(539, 959), (540, 959), (539, 960), (540,960)}
    starting_glom_descriptor = "center 4"
    startingpoints = set()
    starting_points_descriptor = "set()"

else:
    with open("data\\" + prev_run + "\\finalstuff.txt","r") as f:
        starting_glom_descriptor = "Continue from " + prev_run
        starting_points_descriptor = "Continue from " + prev_run
        for i, line in enumerate(f):
            if i == 1:
                startingpoints = literal_eval(line)
            elif i == 3:
                startingglom = literal_eval(line)

# Setting the seed for RNG
randomseed = 42

# Simulation parameters
bounds = (1080,1920)   #the dimensions of the simulation (vert,horiz)
simpoints = 30     #the number of points to simulate simultaneously

# A few handy sets
top = {(0,i) for i in range(bounds[1])}
bottom = {(bounds[0]-1,i) for i in range(bounds[1])}
left = {(i,0) for i in range(bounds[0])}
right = {(i, bounds[1]-1) for i  in range(bounds[0])}

# A set of squares that particles may/must spawn in
spawnsquares = top | bottom | left | right
spawn_squares_descriptor = "edges"   # The parameters log will use this

# Constants for determining when to end the simulation
max_glom = 5000          # Includes starting glom
max_frames = 5000000
time_to_run = 60*60*12  # In seconds


# Constants required for the rendering
dot_sidelength_in_pixels = 1  # Pyplot's DPI setting
animate = 0  # Whether to use pyplot's FuncAnimation to animate the process
interval = 15  # milliseconds between frames if animating

# Set of frames to grab screenshots at
frames_to_snag = {1000000 * i for i in range(1000)}

# Setting the colour map
cbound = [0,1,2,2]
cmap = colors.ListedColormap([[0.15,0,0.2], [0.9,0.9,0.4], [1,0.9,0.7]])
norm = colors.BoundaryNorm(cbound,cmap.N)
