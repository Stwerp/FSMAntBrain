from PyAsciiMaze2 import Game as GameAscii
from PyMazeBrain import Game
import random
import time

from brain_fill_in import antBrain

Graphical = True  # Set this to false for the ascii version

if "Whatever you want" in antBrain.states:
  print('*'*80)
  print('*'*80)
  print(">>>>>> Fill in the 'brain_fill_in.py' file with your ant brain! <<<<<")
  print('*'*80)
  print('*'*80)

if Graphical:
    # VISUAL MODE (needs "pygame" installed)
    #  after running, hit "space" to start autopilot
    diff = 0
    dim = '30x40'
    path = 1

    g = Game(diff, dim, path)
    g.brain = antBrain()
    g.frame_limit = 40
    g.start()
    #g.tickonce_setup()\
else:

    # ASCII MODE
    diff = 0
    dim = '10x10'
    path = 1

    ga = GameAscii(diff, dim, path)
    ga.brain = antBrain()
    ga.start()
    ga.tickonce_setup()
    loop = True  # setting to true makes too much output :()
    if loop:
        while ga.keep_going:
            ga.tickonce('t')
            ga.draw_maze(1)
            time.sleep(.3)
    else:
        ga.tickonce('t')
        ga.draw_maze(1)
