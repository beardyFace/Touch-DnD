import pygame
import math
import os
home = os.path.dirname(os.path.abspath(__file__)) +"\\"

class Tile:
  tile_files  = ['grass', 'ground', 'wall', 'lava', 'ice', 'brick']
  tile_images = {}

  def __init__(self, x, y, z, row, col, depth, width, height, texture):
    self.x = x
    self.y = y
    self.z = z

    self.row   = row
    self.col   = col
    self.depth = depth

    self.width  = width
    self.height = height

    if len(Tile.tile_images) == 0:
      Tile.load_tiles(self.width, self.height)
      
    self.setTexture(texture)

    self.character = None

  def copy(self):
    return Tile(self.x, self.y, self.z, self.row, self.col, self.depth, self.width, self.height, self.texture)
    
  @staticmethod
  def load_tiles(width, height):
    for file in Tile.tile_files:
      # tile = pygame.image.load(home+'blocks/'+file+'.png').convert_alpha()  #load images
      tile = pygame.image.load(home+'blocks/'+file+'.png').convert()  #load images
      tile = pygame.transform.scale(tile, (width, height))

      tile.set_colorkey((0,0,0))
      Tile.tile_images[file] = tile
    
  def draw(self, surface, transparent=False):
    if not self.image == None:
      x_d = self.x - self.width/2
      y_d = self.y - self.height/4
       
      if transparent:
        surface.blit(self.image_transparent, (x_d, y_d))
      else:
        surface.blit(self.image, (x_d, y_d))
    else:
      self.highlightBot(surface, (255, 255, 255), 1)
    self.highlightBot(surface, (255, 255, 255), 1)
    if self.character is not None:
        self.character.draw(surface)

  def highlightBot(self, surface, color=(0, 255, 0), fill=2):
    pts = []
    pts.append((self.x, self.y - self.height/4))#top
    
    pts.append((self.x + self.width/2, self.y))#right
    
    pts.append((self.x, self.y + self.height/4))#bot

    pts.append((self.x - self.width/2, self.y))#left

    pygame.draw.polygon(surface, color, pts, fill)

  def highlightTop(self, surface, color=(0, 255, 0), fill=2):
    pts = []
    pts.append((self.x, self.y - self.height/4 - self.height/2))#top
    
    pts.append((self.x + self.width/2, self.y - self.height/2))#right
    
    pts.append((self.x, self.y + self.height/4 - self.height/2))#bot

    pts.append((self.x - self.width/2, self.y - self.height/2))#left

    pygame.draw.polygon(surface, color, pts, fill)

  def getCharacter(self):
    return self.character

  def isEmpty(self):
    return self.texture == None

  def getTexture(self):
    return self.texture

  def setTexture(self, texture):
    self.texture = texture
    if not self.texture == None:
      self.image = Tile.tile_images[texture]
      self.image_transparent = self.image.copy()
      self.image_transparent.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
    else:
      self.image = None

  def setPose(self, x, y, z, row, col, depth):
    self.x = x
    self.y = y
    self.z = z

    self.row   = row
    self.col   = col
    self.depth = depth

  def getPose(self):
    return self.x, self.y, self.z, self.row, self.col, self.depth

  def removeCharacter(self):
    self.character = None

  def addCharacter(self, character):
    self.character = character
    self.character.setPose(self.x, self.y, self.row, self.col)
