from __future__ import division
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

RPM = 60
FPS = 60


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

        self.is_spinning = False
        self.revolutions = 0
        self.row_rate = None


        self.rect = Rect((0, 0), self.view_size)
        self.screen_rect = Rect(screen_loc, self.view_size)
        self.screen_surface = self.screen.subsurface(self.screen_rect)

        self.load_img(filename)
        self.extend_img()

    def load_img(self, filename):

        image_file = os.path.join(main_dir, filename)
        self.orig_image = pygame.image.load(image_file).convert()

    def extend_img(self):
        """ Increase the size of the image to make infinite scrolling easier """

        # Determine the size of the image
        self.orig_w, self.orig_h = self.orig_image.get_size()

        # Create surface twice as large
        self.image = pygame.Surface((self.orig_w, self.orig_h * 2))

        # Repeat the image
        self.image.blit(self.orig_image, (0, 0))
        self.image.blit(self.orig_image, (0, self.orig_h))

        #self.row_rate = self.orig_h / (FPS * (RPM / 60))
        self.row_rate = 1
        print self.row_rate


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

    def spin(self, revolutions, stop_row):
        """ Spin for a certain amount of time. Duration in milliseconds """

        # Find the distance in px rows
        # (1) What is the distance from the current location to the top?
        # (2) What are the total number of revolutions?
        # (3) What is the distance from the top to the starting point?
        if not self.is_spinning:
            print "SPINNING ====================="
            print "ORIG_H=%i TOP=%i STOP_ROW=%i" % (self.orig_h, self.rect.top, stop_row)
            dist_to_stop = (self.orig_h - self.rect.top) + stop_row
            self.distance = revolutions * self.orig_h + dist_to_stop + revolutions + 1
            self.is_spinning = True
            print "Distance: %i" % self.distance

    def update(self):
        if self.is_spinning:
            #print "Checking dist=%i row_rate=%i top=%i" % (self.distance, self.row_rate, self.rect.top)


            # Check stopping condition
            if self.distance <= 0:
                self.is_spinning = False
                row_rate = 0
                print "STOPPED AT %i" % self.rect.top
            elif self.distance < self.row_rate:
                print "Top %f" % self.distance
                row_rate = self.distance # don't go too far
            else:
                row_rate = self.row_rate

            self.distance -= row_rate
            #print self.distance
            return self.scroll(dy=row_rate)

def main():

    pygame.init()
    pygame.key.set_repeat (20, 20)

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
    clock.tick(FPS)

    going = True
    while going:
        # wait for events before doing anything.
        events = pygame.event.get()

        dirty_rects = []

        dirty_rects.append(r1.update())

        for e in events:

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    going = False
                elif e.key == K_DOWN:
                    dirty_rects.append(r1.scroll(3))
                    dirty_rects.append(r2.scroll(4))
                    dirty_rects.append(r3.scroll(2))
                elif e.key == K_RETURN:
                    r1.spin(3, 640)


            elif e.type == QUIT:
                going = False

        pygame.display.update(dirty_rects)


if __name__ == '__main__':
    main()
