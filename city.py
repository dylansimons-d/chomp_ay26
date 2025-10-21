import pygame
from util_params import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

#################### TESTING ZONE ##########################

grass_tile_location = 'Assets\Tiles/tile_0028.png'
grass_tile = pygame.image.load(grass_tile_location)

#get the tile width, height
tile_width = grass_tile.get_width()
tile_height = grass_tile.get_height()

#make a new surface, background, with the same w,h as screen
background = pygame.Surface((WIDTH, HEIGHT))

# loop over the background and place tiles on it
for x in range(0, WIDTH, tile_width):
    for y in range(0, HEIGHT, tile_height):
        background.blit(grass_tile, (x,y))

#blit the background to our screen
screen.blit(background, (0,0))



#adding horizontal roads
#put these together
h_top_road = 'Assets\Tiles/tile_0##.png'
h_m_road
h_b_road

#make them one 'tile'
h_roads =

#add vertical roads

#add crosswalks for horizontal, and vertical

#add a building


#############################################################


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()