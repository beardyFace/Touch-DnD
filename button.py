import pygame
from pygame.locals import *
import sys
import numpy as np
import os
home = os.path.dirname(os.path.abspath(__file__)) +"\\"

class Button:
  button_files  = ['up-arrow', 'down-arrow', 'left-arrow', 'right-arrow']
  button_images = {}

  def __init__(self, x, y, width, height, texture):
    self.x = x
    self.y = y
    self.width  = width
    self.height = height
    self.texture = texture

    if len(Button.button_images) == 0:
      Button.load_buttons(width, height)
      
    self.setTexture(texture)

  @staticmethod
  def load_buttons(width, height):
    for file in Button.button_files:
      tile = pygame.image.load(home+'gui/'+file+'.png').convert_alpha()  #load images
      tile = pygame.transform.scale(tile, (width, height))
      Button.button_images[file] = tile

  def setTexture(self, texture):
    self.texture = texture
    if not self.texture == None:
      self.image = Button.button_images[texture]
    else:
      self.image = None

  def clicked(self, mx, my):
    return (self.x - self.width/2 <= mx <= self.x + self.width/2) and (self.y - self.height/2 <= my <= self.y + self.height/2) 

  def draw(self, surface):
    surface.blit(self.image, (self.x - self.width/2, self.y - self.height/2))
    # pts = []
    # pts.append([self.x - self.width/2, self.y - self.height/2])#top
    
    # pts.append([self.x + self.width/2, self.y - self.height/2])#right
    
    # pts.append([self.x + self.width/2, self.y + self.height/2])#bot

    # pts.append([self.x - self.width/2, self.y + self.height/2])#left

    # pygame.draw.polygon(surface, (255, 0 ,0), pts, 2)
