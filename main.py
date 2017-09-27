# a script to generate brownian crystals via diffusion limited agaggeration
import random
import os
import configure
import lib
from lib import startlog, endlog, still, render, terminate_condition, advance
# PEP 328 recommends parentheses for multiline imports, and I want to avoid "*"


# The script itself - this line prevents execution when importing
if __name__ == '__main__':

    os.makedirs(lib.path)

    # Setting random seed
    random.seed(configure.config["Random"]["randomseed"])

    # Declaring global variables
    framecount = 0
    particles, agg = set(configure.starting_parts), set(configure.starting_agg)

    startlog()
    # Printing initial data to console
    print("\rDotcount: {0}\tAggsize: {1}\tFramecount: {2:07d}\t".format(
    len(particles), len(agg), 0), end="")

    # Taking a still of the starting conditions
    still(particles, agg, "0")
    # Check to see if it is supposed to animate, if so call the render func
    if configure.animate:
        render(particles, agg)
    # If no animation, then start a while loop that calls the advance func
    else:
        snagframe = next(configure.frames_to_snag)
        while not terminate_condition(framecount, agg):
            particles, agg = advance(particles, agg, framecount)
            framecount += 1
            if framecount == snagframe:
                still(particles, agg, str(framecount))
                snagframe = next(configure.frames_to_snag)

    endlog(particles, agg, framecount)
