from __future__ import print_function
import pygame

pygame.init()

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)

PI = 3.14159

size = (800, 480)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("v1")

done = False
clock = pygame.time.Clock()

bell = pygame.image.load("liberty_bell.png").convert()
bell.set_colorkey(BLACK) # for transparency

reel1 = pygame.image.load("liberty_bell_reel1.png").convert()
reel1.set_colorkey(WHITE) # for transparency

click_sound = pygame.mixer.Sound("laser5.ogg")

i = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            print("keydown")
            print(event)
        elif event.type == pygame.KEYUP:
            print("keyup")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()

    screen.fill(WHITE)
    #pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
    #pygame.draw.rect(screen, BLACK, [20, 20, 250, 100], 2)
    #pygame.draw.ellipse(screen, BLACK, [20,20,250,100], 2)

    #pygame.draw.arc(screen, GREEN, [100,100,250,200],  PI/2,     PI, 2)
    #pygame.draw.arc(screen, BLACK, [100,100,250,200],     0,   PI/2, 2)
    #pygame.draw.arc(screen, RED,   [100,100,250,200],3*PI/2,   2*PI, 2)
    #pygame.draw.arc(screen, BLUE,  [100,100,250,200],    PI, 3*PI/2, 2)

    font = pygame.font.SysFont('Calibri', 25, True, False)
    text = font.render(str(clock.get_fps()), True, BLACK)
    screen.blit(text, [250, 250])

    screen.blit(reel1, [600, 100])

    scroll_jump = -1
    reel1.scroll(dy=scroll_jump)




    pygame.display.flip()
    clock.tick(60)

    i += 1

pygame.quit()
