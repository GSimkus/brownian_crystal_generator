# a script to generate brownian crystals via diffusion limited agglomeration
import re
import random
import csv
import os
from datetime import datetime
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from parameters import (randomseed, bounds, simpoints,
                        spawnsquares, spawn_squares_descriptor,
                        startingglom, starting_glom_descriptor,
                        startingpoints, starting_points_descriptor,
                        max_glom, max_frames, time_to_run,
                        dot_sidelength_in_pixels, animate, interval,
                        frames_to_snag, cbound, cmap, norm)
# PEP 328 recommends parentheses for multiline imports, and I want to avoid "*"

# Begin defining functions
# The neighbors function dictates the possible movements for the particles
def neighbors(point):
    y, x = point
    yield y, x
    yield y + 1, x
    yield y - 1, x
    yield y, x + 1
    yield y, x - 1
    #yield x + 1, y + 1
    #yield x + 1, y - 1
    #yield x - 1, y + 1
    #yield x - 1, y - 1

# Termination condition logic
def by_frames():
    return framecount >= max_frames

def by_glom_size():
    return len(glom) >= max_glom

def by_time_elapsed():
    return t_elapsed() >= time_to_run

terminate_condition = by_time_elapsed
# End termination logic

# Point spawing logic
def random_spawn_to_max():
    freespaces = spawnsquares - points - glom
    while len(points) < simpoints and freespaces:
        points.add(random.sample(freespaces, 1)[0])
        freespaces -= points

def random_spawn_by_frames():
    freespaces = spawnsquares - points - glom
    if freespaces and framecount % 250 == 0:
        points.add(random.sample(freespaces, 1)[0])

spawnpoints = random_spawn_to_max
# End point spawning logic

# Functions that return Bools
def t_elapsed():
    deltatime = datetime.now() - starttime
    return deltatime.total_seconds()

def inbounds(point):
    y, x = point
    return not (x<0 or y <0 or x >= bounds[1] or y >= bounds[0])

# Functions for writing data to disc
def csvsave(point):
    y, x = point
    with open(path + "data.csv", 'a', newline='') as fp:
        a = csv.writer(fp)
        data = [x, y, len(glom), framecount, t_elapsed()]
        a.writerow(data)

def still(points, glom, filename):
    buildfig(points, glom)
    filepath = path + str(filename)
    plt.savefig(filepath)
    print("Saved still as {}.png at time: {:.3f}".format(filepath,t_elapsed()))
    plt.close()

# Funtions for rendering the board
def makematrix(board):
    newboard = np.zeros(bounds).astype(int)
    for cell in board:
        newboard[cell] = True
    return newboard

def buildfig(points, glom, dpi=dot_sidelength_in_pixels):
    X = np.add(makematrix(points), 2*makematrix(glom))
    fig = plt.figure(figsize=(X.shape[1]/4, X.shape[0]/4), dpi=dpi*4)
    ax = fig.add_axes([0, 0, 1, 1], frameon=True)
    im = plt.imshow(X, cmap = cmap, interpolation='nearest', norm=norm)
    return fig, im

# The animation function
def render(points, glom, frames=100, interval=17, mode='loop'):
    fig, im = buildfig(points, glom)

    def init():
        return (im,)

    # animation function.  This is called sequentially
    def animate(i):
        global points, glom
        im.set_data(np.add(makematrix(points), 2*makematrix(glom)))
        points, glom = advance(points, glom)
        return (im,)

    def framer():
        while not terminate_condition():
            yield 1

    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=framer,
                                   interval=interval, repeat = False, blit=True)
    plt.show()

# Core logic for advancing the board
def advance(parts, glom):
    # Determines whether it's necessary to spawn particles
    if len(points) < simpoints:
        spawnpoints()

    newparts = set()
    while parts:
        point = next(iter(parts)) #A handy way to grab a single set element
        possiblemoves = []
        for option in neighbors(point):
            if (not option in (parts | newparts)) and inbounds(option):
                possiblemoves.append(option)
        move = random.choice(possiblemoves)

        if move in glom:
            glom.add(point)
            csvsave(point)
        else:
            newparts.add(move)
        parts.remove(point)

    global framecount
    framecount += 1

    print("\rDotcount: {0}\tGlomsize: {1}\tFramecount: {2:07d}\t".format(
    len(newparts), len(glom), int(framecount)), end="")

    if framecount in frames_to_snag:
        still(newparts, glom, str(framecount))

    return newparts, glom

# The script itself - this line prevents execution when importing
if __name__ == '__main__':

    # Setting random seed
    random.seed(randomseed)

    # Getting the starting time as a datetime object and a string
    starttime = datetime.now()
    starttimestr = starttime.strftime("%Y.%m.%d.%H.%M")

    # Creating a directory to save things in
    path = str("data\\" + starttimestr+"\\")
    os.makedirs(path)

    # Declaring global variables
    framecount = 0
    points, glom = set(startingpoints), set(startingglom)


    # Create the datafile, title the columns, input initial data
    with open(path + "data.csv", 'w', newline='') as f:
        a = csv.writer(f)
        a.writerow(['Glom X','Glom Y',
        'glomsize', 'frame', 'elapsed time'])
        data = ["Start", "Start",
        len(glom), framecount , t_elapsed()]
        a.writerow(data)
    print("Data.csv created in " + path)

    # Creating a parameters file
    with open(path + "params.txt", "w") as f:
        f.write(re.sub('        ','',"""\
        RNG seed: {}
        Bounds (Vert, Horiz): {}
        Max Points Simulated: {}
        Starting Glom: {}
        Starting Points: {}
        Spawning Squares: {}
        Spawning Rules: {}
        Terminate Condition: {}
        Max Glom: {}
        Max Frames: {}
        Run Time: {}\
        """.format(randomseed, bounds, simpoints, starting_glom_descriptor,
                   starting_points_descriptor, spawn_squares_descriptor,
                   spawnpoints.__name__, terminate_condition.__name__, max_glom,
                   max_frames, time_to_run)
                   ))
    print("Parameters logged in " + path)

    # Printing initial data to console
    print("\rDotcount: {0}\tGlomsize: {1}\tFramecount: {2:07d}\t".format(
    len(points), len(glom), int(framecount)), end="")

    # Taking a still of the starting conditions
    still(points, glom, "start")

    # Check to see if it is supposed to animate, if so call the render func
    if animate == 1:
        render(points, glom, interval)
    # If no animation, then start a while loop that calls the advance func
    else:
        while not terminate_condition():
            points, glom = advance(points, glom)

    # At the end of the run take a final still and and save the data to CSV
    still(points, glom, "end")
    csvsave(("End", "End"))

    #Enter the completed run's parameters into the log file in the main dir

    with open("log.txt", "a") as f:
        f.write("{0} Simpoints: {1}\tGlomsize: {2}"
                "\tFramecount: {3:07d}\tRuntime: {4}\n".format(
                starttimestr, simpoints, len(glom), framecount, t_elapsed())
                )
    with open(path + "finalstuff.txt", "w") as f:
        f.write("Particles:\n" + str(points) + "\nGlom: \n" + str(glom))
