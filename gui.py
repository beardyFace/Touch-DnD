import pygame
from pygame.locals import *
import sys
import numpy as np
import os
home = os.path.dirname(os.path.abspath(__file__)) +"\\"

from button import Button
from text_box import InputBox

class GUI:
  
  def __init__(self, x, y, w, h):
    self.x = x
    self.y = y
    self.gui_surface = pygame.Surface((w, h))

    arrow_pose = (x + 100, y + 100)
    arrow_size = 50
    
    self.button_up    = Button(arrow_pose[0], arrow_pose[1] - arrow_size, arrow_size, arrow_size, "up-arrow")
    self.button_down  = Button(arrow_pose[0], arrow_pose[1] + arrow_size, arrow_size, arrow_size, "down-arrow")
    self.button_right = Button(arrow_pose[0] + arrow_size, arrow_pose[1], arrow_size, arrow_size, "right-arrow")
    self.button_left  = Button(arrow_pose[0] - arrow_size, arrow_pose[1], arrow_size, arrow_size, "left-arrow")

    input_pose = (x + arrow_pose[0], y + arrow_pose[1] + 100)
    input_size = (50, 32)

    self.input_width  = InputBox(input_pose[0] - input_size[0]/2, input_pose[1], input_size[0], input_size[1], True, '1')
    self.input_height = InputBox(input_pose[0] - input_size[0]/2, input_pose[1]  + input_size[1], input_size[0], input_size[1], True, '1')

  def handle_event(self, event):
    pass

  def draw(self, surface):
    self.gui_surface.fill(pygame.Color('green'))
    surface.blit(self.gui_surface, (self.x, self.y))