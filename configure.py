import configparser
import math
from itertools import count
from ast import literal_eval
from matplotlib import colors

# Importing the config and assigning global variables
config = configparser.ConfigParser()
config.read("config.ini")

# This section deals with the parameters for ending the simulation
# The dict() makes a copy of the current config's termination settings as a dict
termination = dict(config["Termination"])
termination_condition = termination["terminate_condition"]
terminator = eval(termination["max_" + termination_condition])

# These are used in drawing stills and rendering the animate function
# The dict() makes a copy of the current config's rendering settings as a dict
rendering = dict(config["Rendering"])
cbound = literal_eval(rendering["cbound"])
cmap = colors.ListedColormap(literal_eval(rendering["cmap"]))
norm = colors.BoundaryNorm(cbound,cmap.N)
dpi = int(rendering["dot_sidelength_in_pixels"])
interval = int(rendering["interval"])
frames_to_snag = eval(rendering["frames_to_snag"])
animate = config["Rendering"].getboolean("animate")

# Aliasing the squares and cardinals sections of the config.ini
squares, cardinals = config["Squares"], config["Cardinals"]
board = config["Board"]
# Determining whether to load a previous run's config file and final boardstate
if config["Resume"].getboolean("continue_previous_run"):
    prev_run = config["Resume"]["prev_run"]
    # Loading the previous run's configuration file
    config.read("data\\" + prev_run + "\\config.ini")
    bounds = literal_eval(board["bounds"])
    # Re-inserting the Termination and Rendering dicts to the config
    config.read_dict({"Termination" : termination, "Rendering" : rendering})
    # Loading the "finalstuff" from the previous run
    with open("data\\" + prev_run + "\\finalstuff.txt","r") as f:
        for i, line in enumerate(f):
            if i == 1:
                # Loading the final state of the previous particles
                starting_parts = literal_eval(line)
            elif i == 3:
                #  Loading the final state of the previous aggregate
                starting_agg = literal_eval(line)
else:
    bounds = literal_eval(board["bounds"])
    starting_parts = eval(cardinals[squares["starting_parts"]])
    starting_agg = eval(cardinals[squares["starting_agg"]])


simult_parts = int(board["simult_parts"])
spawnsquares = eval(cardinals[squares["spawnsquares"]])

sticky_agg = config["Aggregate"].getboolean("sticky")
self_aggregate = config["Aggregate"].getboolean("self_aggregate")
neighbors = config["Movement"]["movement_options"]

randomseed = config
