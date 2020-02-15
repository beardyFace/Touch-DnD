import pygame
import math
import os
home = os.path.dirname(os.path.abspath(__file__)) +"\\"

from dungeon import Dungeon
from tile import Tile

VIEW = 0
BUILD = 1
ADD_CHARACTER = 2

SMALL  = 10
MEDIUM = 20
LARGE  = 30
HUGE   = 40

def createRandomDungeon(cube_w, cube_h, map_width, map_height, map_depth, map_pose_x, map_pose_y):
  dungeon = Dungeon(cube_w, cube_h, map_width, map_height, map_depth, map_pose_x, map_pose_y)
  
  # gap = 2
  # size = 10
  # x_i = map_width - size
  # y_i = map_height - size
  # for n in range(0, 20):
  #   createRoom(dungeon, x_i, y_i, size, size, map_depth, 'ground', 'wall')
  #   x_i -= (size + gap)
  #   if x_i < 0:
  #     x_i = map_width - size
  #     y_i -= (size + gap)
  #     if y_i < 0:
  #       break
  return dungeon

def createRoom(dungeon, x_p, y_p, width, length, map_depth, floor_tile, wall_tile):
  cube_w, cube_h = dungeon.getTileSize()
  for x_i in range(x_p, x_p + width):
      for y_i in range(y_p, y_p + length):
          for z_i in range(0, map_depth):
              x_m, y_m, z_m = dungeon.getPose(x_i, y_i, z_i)
              tile = None
              if z_i == 0:
                tile = Tile(x_m, y_m, z_m, x_i, y_i, z_i, cube_w, cube_h, floor_tile)
              elif z_i > 0 and (x_i - x_p == 0 or y_i - y_p ==0):
                tile = Tile(x_m, y_m, z_m, x_i, y_i, z_i, cube_w, cube_h, wall_tile)
              else:
                tile = Tile(x_m, y_m, z_m, x_i, y_i, z_i, cube_w, cube_h, None)
              dungeon.addBlock(x_i, y_i, z_i, tile)

def load(file_path):
  stat_file = open(file_path,'r')
  dungeon_size = stat_file.readline()
  sizes = dungeon_size.split(" ")
  
  map_width  = int(sizes[0])
  map_height = int(sizes[1])
  map_depth  = int(sizes[2])
  map_pose_x = float(sizes[3])
  map_pose_y = float(sizes[4])
  cube_w     = int(sizes[5])
  cube_h     = int(sizes[6])

  dungeon = Dungeon(cube_w, cube_h, map_width, map_height, map_depth, map_pose_x, map_pose_y)

  for z_i in range(0, map_depth):
    for y_i in range(0, map_height):
      row = stat_file.readline()
      row = row.split(",")
      for x_i in range(0, map_width):
        x_m, y_m, z_m = dungeon.getPose(x_i, y_i, z_i)
        row[x_i] = row[x_i].strip('\n')
        if row[x_i] == "None":
          row[x_i] = None
        tile = Tile(x_m, y_m, z_m, x_i, y_i, z_i, cube_w, cube_h, row[x_i])
        dungeon.addBlock(x_i, y_i, z_i, tile)

  return dungeon
