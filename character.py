import os
import pygame

class Character:

  def __init__(self, txt_file, image_file, size):
    self.name  = ""
    self.headers = ""
    self.attributes = ""
    self.stat_block = ""
    self.traits = ""
    self.description = ""
    self.actions = ""
    self.legedary_actions = ""
    self.info = ""
    self.loadDetails(txt_file)
    self.image = pygame.image.load(image_file).convert()
    self.image = pygame.transform.scale(self.image, (size, size))

    self.x = 0
    self.y = 0
    self.row = 0
    self.col = 0
    self.size = (size, size)

  def toFullString(self):
    s  = self.name + "\n\n"
    s += self.headers + "\n\n"
    s += self.attributes + "\n\n"
    s += self.stat_block + "\n\n"
    s += self.traits + "\n\n"
    s += self.description + "\n\n"
    s += self.actions + "\n\n"
    s += self.legedary_actions + "\n\n"
    s += self.info
    return s

  def toShortString(self):
    s  = "Attributes:" + "\n\n"
    s += self.attributes + "\n\n"
    s += "Stats:" + "\n\n"
    s += self.stat_block + "\n\n"
    s += "Actions:" + "\n\n"
    s += self.actions + "\n\n"
    if self.legedary_actions is not "":
      s += "Legendary Actions:" + "\n\n"
      s += self.legedary_actions + "\n\n"
    return s


  def loadDetails(self, txt_file):
    char_file  = open(txt_file, 'r', encoding="utf-8")
    lines = ""
    for line in char_file.readlines():
      lines += line
    split_lines = lines.split('\n\n')

    self.name        = split_lines[0]
    self.headers     = split_lines[1].replace('Headers', '').strip()
    self.attributes  = split_lines[2].replace('Attributes', '').strip()
    self.stat_block  = split_lines[3].replace('Stat-Block', '').strip()
    self.traits      = split_lines[4].replace('Traits', '').strip()
    
    t = split_lines[5] + '#end_info'
    self.description = t[t.index('Description') : t.index('Actions')].strip('\n')
    
    if "Legendary Actions" in split_lines[5]:
      self.actions          = t[t.index('Actions') : t.index('Legendary Actions')]
      self.legedary_actions = t[t.index('Legendary Actions') : t.index('#end_info')].strip('\n')
      self.legedary_actions = self.legedary_actions.replace('Legendary Actions', '').strip('\n')
    else:
      self.actions = t[t.index('Actions') : t.index('#end_info')].strip()
    self.actions = self.actions.replace('Actions', '').strip('\n')

    self.info        = split_lines[6].strip()    

  def draw(self, surface):
    surface.blit(self.image, (self.x - self.size[0]/2, self.y - self.size[1]/2))

  def getPose(self):
    return self.x, self.y, self.row, self.col

  def getSize(self):
    return self.size

  def setPose(self, x, y, row, col):
    self.x = x
    self.y = y
    self.row = row
    self.col = col

  def clicked(self, mx, my):
    return (mx < self.x + self.size[0]/2 and mx > self.x - self.size[0]/2) and (my < self.y + self.size[1]/2 and my > self.y - self.size[1]/2)

  def blitText(self, surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
    return y

  def getTextHeight(self, text, font, max_width):
    # words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    
    x, y = (0, 0)
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, (0,0,0))
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = 0
                y += word_height  # Start on new row.
            x += word_width + space
        x = 0
        y += word_height  # Start on new row.
    return y
        
  def getInfoScreen(self, max_width, max_height):
    text = self.toShortString()
    font = 'Arial'
    font_size = 16

    font_py = pygame.font.SysFont(font, font_size)
    font_py_bold = pygame.font.SysFont(font, font_size, bold=True)

    text_height = 0
    bold = True
    for line in text.split('\n\n'):
      if bold:
        text_height += self.getTextHeight(line+'\n', font_py_bold, max_width)
      else: 
        text_height += self.getTextHeight(line+'\n\n', font_py, max_width)
      bold = not bold

    surface = pygame.Surface((max_width, text_height))
    surface.fill(pygame.Color('white'))
    
    y = 0
    bold = True
    for line in text.split('\n\n'):
      if bold:
        y = self.blitText(surface, line+'\n', (0, y), font_py_bold)
      else: 
        y = self.blitText(surface, line+'\n\n', (0, y), font_py)
      bold = not bold

    return surface
