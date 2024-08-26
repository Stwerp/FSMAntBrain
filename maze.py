from random import shuffle
import random
"""Contains the Maze class which is the array-represented maze."""

class Maze:

  def __init__(self, rows=30, cols=40):

    self.rows = rows
    self.cols = cols
    self.keep_going = 1

    self.maze = {}
    for y in range(rows):
      for x in range(cols):
        cell = {'south' : 1, 'east' : 1, 'visited': 0}
        self.maze[(x,y)] = cell

  def generate(self, start_cell=None):
    """Generates a random maze using a magical simple recursive function."""
    self.rgenerate(start_cell, [])
  
  def rgenerate(self, start_cell=None, stack=[]):
    """Workhorse for generating a random maze using a magical simple recursive function."""

    if start_cell is None:
      start_cell = self.maze[(self.cols-1, self.rows-1)]
    
    if not self.keep_going:
      return

    self.check_finished()
    neighbors = []

    # if the stack is empty, add the start cell
    if len(stack) == 0:
      stack.append(start_cell)

    # set current cell to last cell
    curr_cell = stack[-1]

    # get neighbors and shuffle 'em up a bit
    neighbors = self.get_neighbors(curr_cell)
    shuffle(neighbors)

    for neighbor in neighbors:
      if neighbor['visited'] == 0:
        neighbor['visited'] = 1
        stack.append(neighbor)
        self.knock_wall(curr_cell, neighbor)

        self.rgenerate(start_cell, stack)

  def get_coords(self, cell):
    # grabs coords of a given cell
    coords = (-1, -1)
    for k in self.maze:
      if self.maze[k] is cell:
        coords = (k[0], k[1])
        break
    return coords

  def get_neighbors(self, cell):
    # obvious
    neighbors = []

    (x, y) = self.get_coords(cell)
    if (x, y) == (-1, -1):
      return neighbors

    north = (x, y-1)
    south = (x, y+1)
    east = (x+1, y)
    west = (x-1, y)
    
    if north in self.maze:
      neighbors.append(self.maze[north])
    if south in self.maze:
      neighbors.append(self.maze[south])
    if east in self.maze:
      neighbors.append(self.maze[east])
    if west in self.maze:
      neighbors.append(self.maze[west])

    return neighbors

  def knock_wall(self, cell, neighbor):
    # knocks down wall between cell and neighbor.
    xc, yc = self.get_coords(cell)
    xn, yn = self.get_coords(neighbor)

    # Which neighbor?
    if xc == xn and yc == yn + 1:
      # neighbor's above, knock out south wall of neighbor
      neighbor['south'] = 0
    elif xc == xn and yc == yn - 1:
      # neighbor's below, knock out south wall of cell
      cell['south'] = 0
    elif xc == xn + 1 and yc == yn:
      # neighbor's left, knock out east wall of neighbor
      neighbor['east'] = 0
    elif xc == xn - 1 and yc == yn:
      # neighbor's right, knock down east wall of cell
      cell['east'] = 0

  def check_finished(self):
    # Checks if we're done generating
    done = 1
    for k in self.maze:
      if self.maze[k]['visited'] == 0:
        done = 0
        break
    if done:
      self.keep_going = 0

  def randomize_maze(self, NumberRandomCells=10):
    #NumberRandomCells = 10
    for x in range(NumberRandomCells):
      rx = random.randint(0,self.rows-2)
      ry = random.randint(0,self.cols-2)
      wall = 'south' if random.random() > 0.5 else 'east'
      #self.maze[(ry,rx)][wall] ^= 1
      self.maze[(ry,rx)][wall] = 0

  def ascii(self):
    tbl = '_' + '__'*self.cols
    print(tbl)
    for y in range(self.rows):
      tbl = '|'
      for x in range(self.cols):
        if self.maze[(x,y)]['south']:
          tbl = tbl + '_'
        else:
          tbl = tbl + ' '
        if self.maze[(x,y)]['east']:
          tbl = tbl + "|"
        else:
          tbl = tbl + " "
      print(tbl)
