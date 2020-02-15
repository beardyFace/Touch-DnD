import pygame
from pygame.locals import *
import sys
import numpy as np
import os
home = os.path.dirname(os.path.abspath(__file__)) +"\\"

from tile import Tile

class Dungeon:
  
  def __init__(self, cube_w, cube_h, map_width, map_height, map_depth, map_pose_x, map_pose_y):
    scale = 1
    self.cube_w     = int(cube_w * scale)
    self.cube_h     = int(cube_h * scale)
    self.cube_h_h   = int(cube_h / 2)
    self.cube_w_h   = self.cube_w / 2
    self.cube_h_q = self.cube_h_h / 2

    self.map_width  = map_width
    self.map_height = map_height
    self.map_depth  = map_depth 

    self.map_pose_x = map_pose_x
    self.map_pose_y = map_pose_y

    self.x_h_i = -1
    self.y_h_i = -1
    self.z_h_i = -1

    self.map_blocks = self.createBaseDungeon(self.map_width, self.map_height, self.map_depth)

    self.floor_blocks = []
    for x_i in range(0, map_width):
        x_blocks = []
        for y_i in range(0, map_height):
            z_i = -1
            x_m, y_m, z_m = self.getPose(x_i, y_i, z_i)
            tile = Tile(x_m, y_m, z_m, x_i, y_i, z_i, self.cube_w, self.cube_h, None)
            x_blocks.append(tile)
        self.floor_blocks.append(x_blocks)

  def getSize(self):
    return self.map_width, self.map_height, self.map_depth

  def getTileSize(self):
    return self.cube_w, self.cube_h

  def getBlocks(self):
    return self.map_blocks

  def addBlock(self, x_i, y_i, z_i, tile):
    self.map_blocks[x_i][y_i][z_i] = tile

  def inRange(self, x_i, y_i, z_i):
    return 0 <= x_i < self.map_width and 0 <= y_i < self.map_height and 0 <= z_i < self.map_depth

  def getTile(self, x_i, y_i, z_i):
    if 0 <= x_i < self.map_width and 0 <= y_i < self.map_height and 0 <= z_i < self.map_depth:
      return self.map_blocks[x_i][y_i][z_i]
    return None

  def setHighlight(self, x_i, y_i, z_i):
    self.x_h_i = x_i
    self.y_h_i = y_i
    self.z_h_i = z_i

  def draw(self, surface, mode, new_tiles=None):
    # for c in range(0, self.map_width):
    #   for r in range(0, self.map_height):
    #     self.floor_blocks[r][c].draw(surface)

    for d in range(0, self.map_depth):
        for c in range(0, self.map_height): 
          for r in range(0, self.map_width):
              if not self.map_blocks[r][c][d].isEmpty():
                self.map_blocks[r][c][d].draw(surface, False)#mode==1)
              elif d == 0:
                self.map_blocks[r][c][d].draw(surface, False)#mode==1)

              if self.x_h_i == r and self.y_h_i == c and self.z_h_i == d:
                # if self.z_h_i + 1 == self.map_depth and not self.map_blocks[r][c][d].isEmpty():
                # if not self.map_blocks[r][c][d].isEmpty():
                #     self.map_blocks[r][c][d].highlightTop(surface, pygame.Color('green'), 0)
                # else:
                self.map_blocks[r][c][d].highlightBot(surface, pygame.Color('blue'), 0)

              if len(new_tiles) > 0:
                for h in range(0, len(new_tiles)):
                  for w in range(0, len(new_tiles[h])):
                    _, _, _, x_n, y_n, z_n = new_tiles[h][w].getPose()
                    if x_n == r and y_n == c and z_n == d:
                      new_tiles[h][w].draw(surface, True)

  def getIndex(self, mx, my):
    x_m = y_m = z_m = -1
    for bz in reversed(range(0, self.map_depth)):
    # for bz in range(0, self.map_depth):
      x_m = ((mx - self.map_pose_x) / self.cube_w_h + (my - self.map_pose_y + (bz * self.cube_h_q)) / self.cube_h_q) / 2
      y_m = ((my - self.map_pose_y + (bz * self.cube_h_q)) / self.cube_h_q - (mx - self.map_pose_x) / self.cube_w_h) / 2
      x_i = round(x_m)
      y_i = round(y_m)
      z_i = round(bz)

      if self.inRange(x_i, y_i, z_i):
        if not self.map_blocks[x_i][y_i][z_i].isEmpty():
          break
    if not self.inRange(x_i, y_i, z_i):
      x_i = y_i = z_i = -1
    return x_i, y_i, z_i

  def getPose(self, x_i, y_i, z_i):
    x = (x_i * self.cube_w_h)   - (y_i * self.cube_w_h)   + self.map_pose_x
    y = (y_i * self.cube_h_q) + (x_i * self.cube_h_q) - (z_i * self.cube_h_q) + self.map_pose_y
    z = z_i
    return x, y, z

  def createBaseDungeon(self, map_width, map_height, map_depth):
    map_blocks = []
    for x_i in range(0, map_width):
        x_blocks = []
        for y_i in range(0, map_height):
            y_blocks = []
            for z_i in range(0, map_depth):
                x_m, y_m, z_m = self.getPose(x_i, y_i, z_i)
                tile = Tile(x_m, y_m, z_m, x_i, y_i, z_i, self.cube_w, self.cube_h, None)
                y_blocks.append(tile)
            x_blocks.append(y_blocks)
        map_blocks.append(x_blocks)
    return map_blocks

  def save(self):
    file_path = home + "dungeon.txt"
    stat_file = open(file_path,'w')

    map_data = str(self.map_width) + " " + str(self.map_height) + " " + str(self.map_depth) + " " + str(self.map_pose_x) + " " + str(self.map_pose_y) + " " + str(self.cube_w) + " " + str(self.cube_h)
    stat_file.write(map_data+"\n")

    txt = ""
    for d in range(0, self.map_depth):
      for c in range(0, self.map_height):
        row = ""
        for r in range(0, self.map_width):
          # tile = self.map_blocks[r][c][d].toString()
          tile = self.map_blocks[r][c][d].getTexture()
          if tile == None:
            tile = "None"
          row += tile + ","
        row = row.strip(",")
        stat_file.write(row+"\n")
    stat_file.close()
    