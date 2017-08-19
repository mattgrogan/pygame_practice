#!/usr/bin/env python

"""An zoomed image viewer that demonstrates Surface.scroll
This example shows a scrollable image that has a zoom factor of eight.
It uses the Surface.scroll function to shift the image on the display
surface. A clip rectangle protects a margin area. If called as a function,
the example accepts an optional image file path. If run as a program
it takes an optional file path command line argument. If no file
is provided a default image file is used.
When running click on a black triangle to move one pixel in the direction
the triangle points. Or use the arrow keys. Close the window or press ESC
to quit.
"""

import sys
import os

import pygame
#from pygame.transform import scale
from pygame.locals import *

main_dir = os.path.dirname(os.path.abspath(__file__))

DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4

view_size = (128, 128)
win_size = (800, 480)

reel1_loc = (100, 100)
reel2_loc = (250, 100)
reel3_loc = (500, 100)

background_color = Color('beige')
image1_filename = "liberty_bell_reel1.png"
image2_filename = "liberty_bell_reel2.png"
image3_filename = "liberty_bell_reel3.png"


def scroll_view(screen, image, view_rect):
    #image_w, image_h = image.get_size()

    #if view_rect.bottom + 1 < image_h:
    new_view_rect = view_rect.move(0, 1)
    if image.get_rect().contains(new_view_rect):
        view_rect.move_ip(0, 1)

    screen.blit(image.subsurface(view_rect), (0,0))

def main():

    image1_file = os.path.join(main_dir, image1_filename)
    image2_file = os.path.join(main_dir, image2_filename)
    image3_file = os.path.join(main_dir, image3_filename)

    pygame.init()
    pygame.key.set_repeat (1, 1)

    screen = pygame.display.set_mode(win_size)
    screen.fill(background_color)
    pygame.display.flip()

    image1 = pygame.image.load(image1_file).convert()
    image2 = pygame.image.load(image2_file).convert()
    image3 = pygame.image.load(image3_file).convert()

    reel1_rect = Rect(reel1_loc, view_size)
    view1_rect = Rect((0, 0), view_size)
    reel2_rect = Rect(reel2_loc, view_size)
    view2_rect = Rect((0, 0), view_size)
    reel3_rect = Rect(reel3_loc, view_size)
    view3_rect = Rect((0, 0), view_size)

    s1 = screen.subsurface(reel1_rect)
    s1.blit(image1.subsurface(view1_rect), (0,0))
    s2 = screen.subsurface(reel2_rect)
    s2.blit(image2.subsurface(view2_rect), (0,0))
    s3 = screen.subsurface(reel3_rect)
    s3.blit(image3.subsurface(view3_rect), (0,0))

    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick()

    going = True
    while going:
        # wait for events before doing anything.
        #events = [pygame.event.wait()] + pygame.event.get()
        events = pygame.event.get()

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    going = False
                elif e.key == K_DOWN:
                    scroll_view(s1, image1, view1_rect)
                    scroll_view(s2, image2, view2_rect)
                    scroll_view(s3, image3, view3_rect)

                    pygame.display.update([reel1_rect, reel2_rect, reel3_rect])

            elif e.type == QUIT:
                going = False

if __name__ == '__main__':
    main()
