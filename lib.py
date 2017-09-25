import random
import csv
from itertools import count
from datetime import datetime
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
import configure
from configure import (bounds, cmap, norm, sticky_agg, self_aggregate,
                       termination_condition, terminator)

# Getting the starting time as a datetime object and a string
starttime = datetime.now()
starttimestr = starttime.strftime("%Y.%m.%d.%H.%M")

# Creating a directory to save things in
path = str("data\\" + starttimestr + "\\")

# Defining functions
def terminate_condition(framecount, agg):
    if termination_condition == 'time':
        return t_elapsed() >= terminator
    elif termination_condition == 'frames':
        return framecount >= terminator
    elif termination_condition == 'agg':
        return len(agg) >= terminator

def neighbors(point):
    y, x = point
    for i in eval(configure.neighbors):
        yield i

# The clock function
def t_elapsed():
    deltatime = datetime.now() - starttime
    return deltatime.total_seconds()

# Functions for rendering the board
def makematrix(board):
    newboard = np.zeros(bounds).astype(int)
    for cell in board:
        newboard[cell] = True
    return newboard

def buildfig(particles, agg, dpi=configure.dpi):
    X = np.add(makematrix(particles), 2*makematrix(agg))
    fig = plt.figure(figsize=(X.shape[1]/4, X.shape[0]/4), dpi=dpi*4)
    ax = fig.add_axes([0, 0, 1, 1], frameon=True)
    im = plt.imshow(X, cmap=cmap, interpolation='nearest', norm=norm)
    return fig, im

def still(particles, agg, filename, path = path):
    buildfig(particles, agg)
    filepath = path + str(filename)
    plt.savefig(filepath)
    print("Saved still {}.png at time: {:.3f}".format(filepath,t_elapsed()))
    plt.close()

# The animation function
def render(particles, agg, interval=configure.interval, mode='loop'):
    fig, im = buildfig(particles, agg, dpi=1)
    counter = count(1)
    snagframe = next(configure.frames_to_snag)

    def init():
        return (im,)

    def animate(i):
        nonlocal particles, agg, snagframe
        if i == snagframe:
            still(particles, agg, str(i))
            snagframe = next(configure.frames_to_snag)
        im.set_data(np.add(makematrix(particles), 2*makematrix(agg)))
        particles, agg = advance(particles, agg, i)
        return (im,)

    def framer():
        while not terminate_condition(counter, agg):
            yield next(counter)

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=framer,
                                   interval=interval, repeat = False, blit=True)
    plt.show()

def csvsave(point, agg, framecount, path = path):
    y, x = point
    with open(path + "data.csv", 'a', newline='') as fp:
        a = csv.writer(fp)
        data = [x, y, len(agg), framecount, t_elapsed()]
        a.writerow(data)

def inbounds(point):
    y, x = point
    return not (x < 0 or
                y < 0 or
                x >= bounds[1] or
                y >= bounds[0]
               )


def spawn_particles(particles, agg):
    freespaces = configure.spawnsquares - particles - agg
    while len(particles) < configure.simult_parts and freespaces:
        particles.add(random.sample(freespaces, 1)[0])
        freespaces -= particles

def movement(particle, agg, particles, newparticles):
    possiblemoves = []
    for option in neighbors(particle):
        if option in agg and sticky_agg == True:
            agg.add(particle)
            return

        elif inbounds(option) and (not option in (particles | newparticles)):
            possiblemoves.append(option)

        elif self_aggregate == True and option in (particles | newparticles):
            agg.add(particle)
            return

    # If all the spaces in neighbors are occupied, then don't move
    if possiblemoves:
        move = random.choice(possiblemoves)
        if move in agg:
            agg.add(particle)
            return
    else:
        move = particle

    return move

def advance(particles, agg, framecount):
    # Determines whether it's necessary to spawn particles
    if len(particles) < configure.simult_parts:
        spawn_particles(particles, agg)

    newparticles = set()
    while particles:
        particle = next(iter(particles)) # A way to grab a single set element
        move = movement(particle, agg, particles, newparticles)
        if not move:
            csvsave(particle, agg, framecount)
            newparticles |= set()
        else:
            newparticles |= {move}
        particles.remove(particle)

    print("\rDotcount: {0}\tAggsize: {1}\tFramecount: {2:07d}\t".format(
    len(newparticles), len(agg), framecount + 1), end="")

    return newparticles, agg


def startlog():
    # Create the datafile, title the columns, input initial data
    with open(path + "data.csv", 'w', newline='') as f:
        a = csv.writer(f)
        a.writerow(['Aggregate X','Aggregate Y',
        'Aggsize', 'frame', 'elapsed time'])
        data = ["Start", "Start",
        len(configure.starting_agg), 0 , t_elapsed()]
        a.writerow(data)
    print("Data.csv created in " + path)

    # recording the config file
    with open(path + "config.ini", "w") as configfile:
        configure.config.write(configfile)
    print("Config logged in " + path)


def endlog(particles, agg, framecount):
    # At the end of the run take a final still and and save the data to CSV
    still(particles, agg, "end")
    csvsave(("End", "End"), agg, framecount)

    with open("log.txt", "a") as f:
        f.write("{0} Simult. Parts: {1}\taggsize: {2}"
                "\tFramecount: {3:07d}\tRuntime: {4}\n".format(starttimestr,
                configure.simult_parts, len(agg), framecount, t_elapsed())
                )
    with open(path + "finalstuff.txt", "w") as f:
        f.write("Particles:\n" + str(particles) + "\nAgg: \n" + str(agg))
