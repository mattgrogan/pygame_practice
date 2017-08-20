import os

import pygame
from pygame.locals import *

main_dir = os.path.dirname(os.path.abspath(__file__))

view_size = (128, 300)
win_size = (800, 480)

reel1_loc = (100, 100)
reel2_loc = (258, 100)
reel3_loc = (416, 100)

background_color = Color('beige')

image1_filename = "liberty_bell_reel1.png"
image2_filename = "liberty_bell_reel2.png"
image3_filename = "liberty_bell_reel3.png"


class Reel(object):
    def __init__(self, filename, screen, screen_loc, view_size):

        self.filename = filename
        self.screen = screen
        self.screen_loc = screen_loc
        self.view_size = view_size

        self.orig_image = None
        self.orig_h = None
        self.orig_w = None

        self.image = None

        self.rect = Rect((0, 0), self.view_size)
        self.screen_rect = Rect(screen_loc, self.view_size)
        self.screen_surface = self.screen.subsurface(self.screen_rect)

        self.load_img(filename)
        self.extend_img()

    def load_img(self, filename):

        image_file = os.path.join(main_dir, filename)
        self.orig_image = pygame.image.load(image_file).convert()

    def extend_img(self):
        """ Increase the size of the image to make scrolling easier """

        # Determine the size of the image
        self.orig_w, self.orig_h = self.orig_image.get_size()

        # Create surface twice as large
        self.image = pygame.Surface((self.orig_w, self.orig_h * 2))

        # Repeat the image
        self.image.blit(self.orig_image, (0, 0))
        self.image.blit(self.orig_image, (0, self.orig_h))

    def get_view(self):

        return self.image.subsurface(self.rect)

    def scroll(self, dy=1):

        if self.rect.top + dy > self.orig_h:
            self.rect.topleft = (0, 0) # Reset to top
        else:
            self.rect.move_ip(0, dy)

        self.blit()
        return self.screen_rect

    def blit(self):
        self.screen_surface.blit(self.get_view(), (0, 0))


def main():

    pygame.init()
    pygame.key.set_repeat (1, 1)

    screen = pygame.display.set_mode(win_size)
    screen.fill(background_color)
    pygame.display.flip()

    r1 = Reel(image1_filename, screen, reel1_loc, view_size)
    r2 = Reel(image2_filename, screen, reel2_loc, view_size)
    r3 = Reel(image3_filename, screen, reel3_loc, view_size)

    r1.blit()
    r2.blit()
    r3.blit()

    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(60)

    going = True
    while going:
        # wait for events before doing anything.
        events = pygame.event.get()

        for e in events:
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    going = False
                elif e.key == K_DOWN:

                    dirty_rects = []

                    dirty_rects.append(r1.scroll())
                    dirty_rects.append(r2.scroll())
                    dirty_rects.append(r3.scroll())

                    pygame.display.update(dirty_rects)

            elif e.type == QUIT:
                going = False

if __name__ == '__main__':
    main()
