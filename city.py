import pygame
from util_params import *
from util_background import *
from car import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

#################### TESTING ZONE ##########################





#############################################################

background = build_background()
screen.blit(background, (0,0))

#grid of car
grid_w, grid_h, cx, cy, tile_w, tile_h = grid_info()

cars = build_car(tile_w, tile_h, cx, cy, WIDTH, HEIGHT, speed = 160)

while running:
    dt = clock.tick(60) / 2000
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    # fill the screen with a color to wipe away anything from last frame
    

    # RENDER YOUR GAME HERE
    screen.blit(background, (0,0))
    for c in cars:
        c.update(dt)
        if c.offscreen(WIDTH, HEIGHT):
            c.reset()
        c.draw(screen)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    # flip() the display to put your work on screen
    pygame.display.flip()

    #clock.tick(60)  # limits FPS to 60

pygame.quit()