#!/usr/bin/python
from sys import argv
from maze import Maze
import random

class Game:

  def __init__(self, diff, dim, path):
    self.diff = diff
    self.dim = map(int, dim.split('x'))
    self.path = path
    self.brain = ''

  def start(self):
    self.maze_obj = Maze(*self.dim)# pass args to change maze size: Maze(10, 10)
    if self.diff == 0:
      self.maze_obj.generate(self.maze_obj.maze[(0,0)])
    else:
      self.maze_obj.generate()
    #self.maze_obj.randomize_maze(600)
    self.maze_obj.randomize_maze(50)
    self.draw_maze()
    self.reset_player()
    #self.loop()

  def reset_player(self):
    # Make the sprites for the player.
    rect = 0, 0
    # Make a same-size matrix for the player.
    self.player_maze = {}
    for y in range(self.maze_obj.rows):
      for x in range(self.maze_obj.cols):
        cell = {'visited' : 0} # if 1, draws green. if >= 2, draws red.
        self.player_maze[(x,y)] = cell
    self.cx = self.cy = 0
    self.curr_cell = self.player_maze[(self.cx, self.cy)] # starts at origin
    self.last_move = None # For last move fun

  def draw_maze(self, player=0):
    if player==0:
        self.maze_obj.ascii()
    else:
        for y in range(self.maze_obj.rows):
            tbl = '|'
            for x in range(self.maze_obj.cols):
                if (self.cx == x) and (self.cy == y):
                    tbl += "\033[4mx\033[0m" if self.maze_obj.maze[(x,y)]['south'] else 'x'
                else:
                    tbl += '_' if self.maze_obj.maze[(x,y)]['south'] else ' '
                tbl += '|' if self.maze_obj.maze[(x,y)]['east'] else ' '
            print(tbl)
    
  def do_ant_stuff(self):
    # Get antenna inputs
    Antenna = self.get_Antenna(self.Dir)
    antMove = self.brain.advance(Antenna)
    # Process output
    if antMove == 'F':
      self.move_player(self.Dir)
      return 1
    if antMove == 'TR':
      self.Dir = {'u':'r','d':'l', 'l':'u', 'r':'d'}[self.Dir]
    if antMove == 'TL':
      self.Dir = {'u':'l','d':'r', 'l':'d', 'r':'u'}[self.Dir]
    return 0

  def loop(self):
    self.keep_going = 1
    self.Dir = 'd'
    while self.keep_going:
      moved = 0
      event = input("? >")
      if event in ['q', 'Q']:
        self.keep_going = 0
      #elif event == 'r' or 'R':
      #  self.reset_player()
      elif event in ['d', 'D']:
        self.move_player('d')
        moved = 1
      elif event in ['u', 'U']:
        self.move_player('u')
        moved = 1
      elif event in ['l', 'L']:
        self.move_player('l')
        moved = 1
      elif event in ['r', 'R']:
        self.move_player('r')
        moved = 1
      elif event in ['t', 'T']:
        moved = self.do_ant_stuff()
      self.draw_player()
    
  def tickonce_setup(self):
    self.keep_going = 1
    self.Dir = 'd'
    self.brain.reset()
    
  def tickonce(self, event):
    moved = 0
    #event = input("? >")
    if not self.keep_going:
        return
    if event in ['q', 'Q']:
      self.keep_going = 0
    #elif event == 'r' or 'R':
    #  self.reset_player()
    elif event in ['d', 'D']:
      self.move_player('d')
      moved = 1
    elif event in ['u', 'U']:
      self.move_player('u')
      moved = 1
    elif event in ['l', 'L']:
      self.move_player('l')
      moved = 1
    elif event in ['r', 'R']:
      self.move_player('r')
      moved = 1
    elif event in ['t', 'T']:
      moved = self.do_ant_stuff()
    self.draw_player()

  def get_Antenna(self, dir):
    below = self.maze_obj.maze[(self.cx, self.cy)]['south']
    right = self.maze_obj.maze[(self.cx, self.cy)]['east']
    if self.cy == 0:
      above = 1
    else:
      above = self.maze_obj.maze[(self.cx, self.cy-1)]['south']
    if self.cx == 0:
      left = 1
    else:
      left  = self.maze_obj.maze[(self.cx-1, self.cy)]['east']
    above = '1' if above else '0'
    below = '1' if below else '0'
    left = '1' if left else '0'
    right = '1' if right else '0'
    
    return {'u':above+right+left,
            'r':right+below+above,
            'd':below+left+right,
            'l':left+above+below}[self.Dir]

  def move_player(self, dir):
    no_move = 0
    try:
      if dir == 'u':
        if not self.maze_obj.maze[(self.cx, self.cy-1)]['south']:
          self.cy -= 1
          self.curr_cell['visited'] += 1
        else: no_move = 1
      elif dir == 'd':
        if not self.maze_obj.maze[(self.cx, self.cy)]['south']:
          self.cy += 1
          self.curr_cell['visited'] += 1
        else: no_move = 1
      elif dir == 'l':
        if not self.maze_obj.maze[(self.cx-1, self.cy)]['east']:
          self.cx -= 1
          self.curr_cell['visited'] += 1
        else: no_move = 1
      elif dir == 'r':
        if not self.maze_obj.maze[(self.cx, self.cy)]['east']:
          self.cx += 1
          self.curr_cell['visited'] += 1
        else: no_move = 1
      else:
        no_move = 1
    except KeyError: # Tried to move outside screen
      no_move = 1


    # Handle last move...
    if ((dir == 'u' and self.last_move == 'd') or \
        (dir == 'd' and self.last_move == 'u') or \
        (dir == 'l' and self.last_move == 'r') or \
        (dir == 'r' and self.last_move == 'l')) and \
        not no_move:
      self.curr_cell['visited'] += 1

    if not no_move:
      self.last_move = dir
      self.curr_cell = self.player_maze[(self.cx, self.cy)]

    # Check for victory.
    if self.cx + 1 == self.maze_obj.cols and self.cy + 1 == self.maze_obj.rows:
      print('Congratumalations, you beat this maze.')
      self.keep_going = 0

  def draw_player(self):
    if 0:
      for y in range(self.maze_obj.rows):
        for x in range(self.maze_obj.cols):
          tbl = '|'
          if self.player_maze[(x,y)]['visited'] > 0:
            if self.player_maze[(x,y)]['visited'] == 1:
              tbl = tbl + '='
            else:
              tbl = tbl +  '*'
              # draw green circles
          else:
            if self.maze_obj.maze[(x,y)]['south']:
              tbl = tbl + '='
            else:
              tbl = tbl + ''
        print(tbl)

if __name__ == '__main__':
  args = argv[1:]
  diff = 0
  dim = '10x10'
  path = 1
  for arg in args:
    if '--diff' in arg:
      diff = int(arg.split('=')[-1])
    elif '--dim' in arg:
      dim = arg.split('=')[-1]
    elif '--path' in arg:
      path = int(arg.split('=')[-1])

  g = Game(diff, dim, path)
  g.start()
