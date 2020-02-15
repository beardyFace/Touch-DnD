import pygame
from pygame.locals import *
import sys
import numpy as np
import os
home = os.path.dirname(os.path.abspath(__file__)) +"\\"

class InputBox:
  COLOR_INACTIVE = pygame.Color('lightskyblue3')
  COLOR_ACTIVE   = pygame.Color('dodgerblue2')
  FONT = pygame.font.Font(None, 32)

  def __init__(self, x, y, w, h, num_only=False, text=''):
      self.rect = pygame.Rect(x, y, w, h)
      self.color = InputBox.COLOR_INACTIVE
      self.text = text
      self.txt_surface = InputBox.FONT.render(text, True, self.color)
      self.active = False
      self.num_only = num_only

  def handle_event(self, event):
      if event.type == pygame.MOUSEBUTTONDOWN:
          # If the user clicked on the input_box rect.
          if self.rect.collidepoint(event.pos):
              # Toggle the active variable.
              self.active = not self.active
          else:
              self.active = False
          # Change the current color of the input box.
          self.color = InputBox.COLOR_ACTIVE if self.active else InputBox.COLOR_INACTIVE
      if event.type == pygame.KEYDOWN:
          if self.active:
              # if event.key == pygame.K_RETURN:
              #     print(self.text)
              #     self.text = ''
              if event.key == pygame.K_BACKSPACE:
                  self.text = self.text[:-1]
              else:
                c = event.unicode
                if not self.num_only:
                  self.text += c
                else:
                  try: 
                    int(c)
                    self.text += c
                  except ValueError:
                    pass
              # Re-render the text.
              self.txt_surface = InputBox.FONT.render(self.text, True, self.color)
      return self.active

  def getText(self):
    return self.text

  def clicked(self, mx, my):
    return self.rect.collidepoint((mx, my))

  def draw(self, surface):
      # Blit the text.
      surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
      # Blit the rect.
      pygame.draw.rect(surface, self.color, self.rect, 2)