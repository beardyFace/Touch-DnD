import pygame
pygame.init()
pygame.font.init()

from pygame.locals import *
import sys
import numpy as np
import os
home = os.path.dirname(os.path.abspath(__file__)) +"\\"

import helper as hlp
from dungeon import Dungeon
from tile import Tile
from button import Button
from text_box import InputBox
from gui import GUI

mode = hlp.VIEW

def getKeyNumber(event):
    if event.key == K_0:
        return 0
    elif event.key == K_1:
        return 1
    elif event.key == K_2:
        return 2
    elif event.key == K_3:
        return 3
    elif event.key == K_4:
        return 4
    elif event.key == K_5:
        return 5
    elif event.key == K_6:  
        return 6
    elif event.key == K_7:
        return 7
    elif event.key == K_8:
        return 8
    elif event.key == K_9:
        return 9
    return None

def main():
    pygame.display.set_caption('Map Rendering Demo')

    # surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    window = pygame.display.set_mode((1600, 1000), DOUBLEBUF)
        
    # hammer = pygame.image.load(home+'hammer.png').convert_alpha()  #load images
    # hammer = pygame.transform.scale(hammer, (25, 25))

    window_width, window_height = pygame.display.get_surface().get_size()
    surface_width  = 2 * window_width
    surface_height = 2 * window_width
    surface = pygame.Surface((surface_width, surface_height))

    clock   = pygame.time.Clock()

    WIDTH, HEIGHT = surface.get_size()
    print(WIDTH)
    print(HEIGHT)

    map_pose_x = WIDTH/2 # start displaying the map from
    map_pose_y = HEIGHT/8 # these window co-ordinates

    cube_w, cube_h = (64, 64)
    scale = 1
    cube_w   = int(cube_w * scale)
    cube_h   = int(cube_h * scale)
    cube_h_h = int(cube_h / 2)
    cube_w_h = cube_w / 2
    cube_h_h_q = cube_h_h / 2

    map_width  = int(surface_width/cube_w)
    map_height = int(surface_height/cube_h)
    map_depth = 4

    print(map_width)
    print(map_height)

    # dungeon = Dungeon(cube_w, cube_h, map_width, map_height, map_depth, map_pose_x, map_pose_y)
    dungeon = hlp.createRandomDungeon(cube_w, cube_h, map_width, map_height, map_depth, map_pose_x, map_pose_y)
    
    dx = -map_pose_x
    dy = -map_pose_y
    print(dx)
    print(dy)
    
    mode = hlp.VIEW
    new_tiles = []

    #GUI
    arrow_pose = (100, 100)
    arrow_size = 50
    button_up    = Button(arrow_pose[0], arrow_pose[1] - arrow_size, arrow_size, arrow_size, "up-arrow")
    button_down  = Button(arrow_pose[0], arrow_pose[1] + arrow_size, arrow_size, arrow_size, "down-arrow")
    button_right = Button(arrow_pose[0] + arrow_size, arrow_pose[1], arrow_size, arrow_size, "right-arrow")
    button_left  = Button(arrow_pose[0] - arrow_size, arrow_pose[1], arrow_size, arrow_size, "left-arrow")

    input_pose = (arrow_pose[0], arrow_pose[1] + 100)
    input_size = (50, 32)
    input_width  = InputBox(input_pose[0] - input_size[0]/2, input_pose[1], input_size[0], input_size[1], True, '1')
    input_height = InputBox(input_pose[0] - input_size[0]/2, input_pose[1]  + input_size[1], input_size[0], input_size[1], True, '1')

    gui = GUI(10, 10, 300, 500)

    while True:
        window.fill(pygame.Color('white'))
        surface.fill(pygame.Color('black'))

        mouse_pos = pygame.mouse.get_pos()
        mx     = mouse_pos[0]
        my     = mouse_pos[1]

        keys = pygame.key.get_pressed()
        step_size = 20
        if keys[pygame.K_RIGHT]:
            dx = dx - step_size
        if keys[pygame.K_LEFT]:
            dx = dx + step_size
        if keys[pygame.K_UP]:
            dy = dy + step_size
        if keys[pygame.K_DOWN]:
            dy = dy - step_size

        mice = pygame.mouse.get_pressed()
        if mice[0]:
          if button_right.clicked(mx, my):
            dx = dx - step_size
          elif button_left.clicked(mx, my):
            dx = dx + step_size
          elif button_up.clicked(mx, my):
            dy = dy + step_size
          elif button_down.clicked(mx, my):
            dy = dy - step_size

        mx_adj = mx - dx
        my_adj = my - dy
            
        x_i, y_i, z_i = dungeon.getIndex(mx_adj, my_adj)
        # x_i_s = str(x_i)
        # y_i_s = str(y_i)
        # z_i_s = str(z_i)
        # print(x_i_s +" "+y_i_s+" "+z_i_s)

        dungeon.setHighlight(x_i, y_i, z_i)
        
        # if dungeon.inRange(x_i, y_i, z_i):
        #     pygame.mouse.set_visible(False)
        # else:
        #   pygame.mouse.set_visible(True)

        if mode == hlp.BUILD:
          if dungeon.inRange(x_i, y_i, z_i):
            if len(new_tiles) > 0:
              for h in range(0, len(new_tiles)):
                for w in range(0, len(new_tiles[h])):
                  x_i_n = x_i + w
                  y_i_n = y_i + h
                  if dungeon.getTile(x_i, y_i, z_i).isEmpty():
                    z_i_n = z_i
                  else:
                    z_i_n = z_i + 1
                  x_m, y_m, z_m = dungeon.getPose(x_i_n, y_i_n, z_i_n)
                  new_tiles[h][w].setPose(x_m, y_m, z_m, x_i_n, y_i_n, z_i_n)

        for event in pygame.event.get():
            if event.type == QUIT:
              pygame.quit()
              sys.exit()

            input_active  = input_width.handle_event(event)
            input_active |= input_height.handle_event(event)
            # elif event.type == KEYUP:
            #     if event.key == K_ESCAPE:
            #         pygame.quit()
            #         sys.exit()
            if not input_active:
              if event.type == KEYDOWN:
                if event.key == K_c:
                  mode = hlp.VIEW
                  new_tiles = []
                  pygame.mouse.set_visible(True)
                elif event.key == K_b:
                  mode = hlp.BUILD
                  new_tiles = []
                  # pygame.mouse.set_visible(False)
                elif mode == hlp.BUILD:
                  number = getKeyNumber(event)
                  if not number == None:
                      if number < len(Tile.tile_files):
                        name = Tile.tile_files[number]
                        w = int(input_width.getText())
                        h = int(input_height.getText())
                        new_width  = max(1, w)
                        new_height = max(1, h)

                        new_tiles = []
                        for h in range(0, new_height): 
                          temp = []
                          for w in range(0, new_width):
                            x_i_n = x_i + w
                            y_i_n = y_i + h
                            z_i_n = z_i + 1
                            x_m, y_m, z_m = dungeon.getPose(x_i_n, y_i_n, z_i_n)
                            temp.append(Tile(x_m, y_m, z_m, x_i_n, y_i_n, z_i_n, cube_w, cube_h, name))
                          new_tiles.append(temp)
                      else:
                          new_tiles = []
                elif event.key == K_s:
                  dungeon.save()
                elif event.key == K_l:
                  file_path = home + "dungeon.txt"
                  dungeon = hlp.load(file_path)

              elif event.type == pygame.MOUSEBUTTONDOWN:
                  if button_up.clicked(mx, my) or button_down.clicked(mx, my) or button_left.clicked(mx, my) or button_right.clicked(mx, my):
                    pass
                  elif mode == hlp.BUILD:
                    if event.button == 1:#Add tiles
                      if len(new_tiles) > 0:
                        for h in range(0, len(new_tiles)):
                          for w in range(0, len(new_tiles[h])):                            
                            t_x, t_y, t_z, x_n, y_n, z_n = new_tiles[h][w].getPose()
                            if dungeon.inRange(x_n, y_n, z_n): 
                              dungeon.addBlock(x_n, y_n, z_n, new_tiles[h][w].copy())

                    elif event.button == 3:#Delete Tile
                      if dungeon.inRange(x_i, y_i, z_i):
                        if dungeon.getTile(x_i, y_i, z_i).isEmpty() and dungeon.inRange(x_i, y_i, z_i - 1):
                          dungeon.getTile(x_i, y_i, z_i - 1).setTexture(None)  
                        else:
                          dungeon.getTile(x_i, y_i, z_i).setTexture(None)

        dungeon.draw(surface, mode, new_tiles)    
        window.blit(surface, (dx,dy))

        # gui.draw(window)
        button_up.draw(window)
        button_down.draw(window)
        button_left.draw(window)
        button_right.draw(window)
        
        input_width.draw(window)
        input_height.draw(window)

        pygame.display.flip()
        pygame.display.update()
        clock.tick(30)

main()