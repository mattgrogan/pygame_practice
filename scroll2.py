from __future__ import division
import os
import random

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

RPM = 90
FPS = 60

class ReelStepper(object):

    def __init__(self, total_steps):
        self.total_steps = total_steps
        self.steps_remaining = 0

    def set_target(self, pos, tgt, revs=0):

        if tgt == pos:
            # Target is the same as current position
            offset = 0
        elif tgt > pos:
            # Target is after the current position
            offset = tgt - pos
        elif tgt < pos:
            # Target is after next revolution
            offset = (self.total_steps - pos) + tgt

        self.steps_remaining = revs * (self.total_steps) + offset

        print "sr=%i pos=%i tgt=%i revs=%i" % (self.steps_remaining, pos, tgt, revs)

    def step(self, steps):

        steps = steps

        if self.steps_remaining <= 0:
            raise ValueError("Steps remaining cannot be negative")
        elif self.steps_remaining <= steps:
            steps = self.steps_remaining

        self.steps_remaining -= steps

        return steps # Actual steps taken



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

        self.reel_stepper = None
        self.is_spinning = False


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

        self.row_rate = self.orig_h / (60 / RPM) / FPS
        #self.row_rate = 1
        self.reel_stepper = ReelStepper(total_steps=self.orig_h)
        print self.row_rate


    def get_view(self):

        return self.image.subsurface(self.rect)

    def scroll(self, dy=1):

        if self.rect.top + dy > self.orig_h:
            y = (self.rect.top + dy) - self.orig_h
            self.rect.topleft = (0, y) # Reset to top
        else:
            self.rect.move_ip(0, dy)

        self.blit()
        return self.screen_rect

    def blit(self):
        self.screen_surface.blit(self.get_view(), (0, 0))

    def spin(self, revolutions, stop_row):
        """ Spin for a certain amount of time. Duration in milliseconds """

        if not self.is_spinning:
            self.reel_stepper.set_target(pos=self.rect.top, tgt=stop_row, revs=revolutions)
            self.is_spinning = True

    def update(self):
        if self.is_spinning:
            try:
                rows = self.reel_stepper.step(self.row_rate)
            except ValueError:
                print "stopping at %i" % self.rect.top
                self.is_spinning = False
                return None

            return self.scroll(dy=rows)

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

    going = True
    while going:
        # wait for events before doing anything.
        events = pygame.event.get()

        dirty_rects = []

        dirty_rects.append(r1.update())
        dirty_rects.append(r2.update())
        dirty_rects.append(r3.update())

        for e in events:

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    going = False
                elif e.key == K_DOWN:
                    dirty_rects.append(r1.scroll(3))
                    dirty_rects.append(r2.scroll(4))
                    dirty_rects.append(r3.scroll(2))
                elif e.key == K_RETURN:
                    r1.spin(3, random.randint(0, r1.orig_h))
                    r2.spin(4, random.randint(0, r2.orig_h))
                    r3.spin(5, random.randint(0, r3.orig_h))


            elif e.type == QUIT:
                going = False

        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render(str(clock.get_fps()), True, Color("black"), Color("white"))
        text_rect = Rect(600, 450, text.get_rect().width, text.get_rect().height)
        screen.blit(text, text_rect)
        dirty_rects.append(text_rect)

        pygame.display.update(dirty_rects)



        clock.tick(FPS)



if __name__ == '__main__':
    main()
