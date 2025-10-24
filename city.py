import pygame
from util_params import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

#################### TESTING ZONE ##########################
SCALE = 2  # 1=16px, 2=32px, 3=48px …


grass_tile_location = 'Assets\Tiles/tile_0028.png'
grass_tile = pygame.image.load(grass_tile_location)

tile_width, tile_height = grass_tile.get_size()
grass_tile = pygame.transform.scale(grass_tile, (grass_tile.get_width()*SCALE, grass_tile.get_height()*SCALE))

#get the tile width, height
tile_width = grass_tile.get_width()
tile_height = grass_tile.get_height()

#make a new surface, background, with the same w,h as screen
background = pygame.Surface((WIDTH, HEIGHT))

# loop over the background and place tiles on it
for x in range(0, WIDTH, tile_width):
    for y in range(0, HEIGHT, tile_height):
        background.blit(grass_tile, (x,y))


#adding roads

def load_tile(idx):
    return pygame.transform.scale(pygame.image.load(f"Assets/Tiles/tile_{idx:04}.png").convert_alpha(), (tile_width, tile_height))

# Kenney road IDs
H_T, H_M, H_B = 406, 433, 460   # horizontal: top, middle (dashed), bottom
V_L, V_M, V_R = 461, 462, 463   # vertical:   left, middle (dashed), right

def paint_h_road(surf, cy, x0, x1):
    for x in range(x0, x1+1):
        surf.blit(load_tile(H_T), (x*tile_width, (cy-1)*tile_height))
        surf.blit(load_tile(H_M), (x*tile_width,  cy   *tile_height))
        surf.blit(load_tile(H_B), (x*tile_width, (cy+1)*tile_height))

def paint_v_road(surf, cx, y0, y1):
    for y in range(y0, y1+1):
        surf.blit(load_tile(V_L), ((cx-1)*tile_width, y*tile_height))
        surf.blit(load_tile(V_M), ( cx   *tile_width, y*tile_height))
        surf.blit(load_tile(V_R), ((cx+1)*tile_width, y*tile_height))


gx, gy = WIDTH//tile_width, HEIGHT//tile_height
cx, cy =gx//2, gy//2
paint_h_road(background, cy, 0, gx-1)
paint_v_road(background, cx, 0, gy)

#Crosswalks
H_XW_T, H_XW_M, H_XW_B = 434, 435, 436 #horizonatal cross walk
V_XW_L, V_XW_M, V_XW_R = 405, 432, 459

def paint_crosswalks_around(surf, cx, cy, offset = 2):
    #horizontal crosswalks
    surf.blit(load_tile(H_XW_T), ((cx-1)*tile_width, (cy-offset)*tile_height))
    surf.blit(load_tile(H_XW_M), ( cx *tile_width, (cy-offset)*tile_height))
    surf.blit(load_tile(H_XW_B), ((cx+1)*tile_width, (cy-offset)*tile_height))

    surf.blit(load_tile(H_XW_T), ((cx-1)*tile_width, (cy+offset)*tile_height))
    surf.blit(load_tile(H_XW_M), ( cx *tile_width, (cy+offset)*tile_height))
    surf.blit(load_tile(H_XW_B), ((cx+1)*tile_width, (cy+offset)*tile_height))

    #vertical crosswalks
    surf.blit(load_tile(V_XW_L), ((cx-offset)*tile_width, (cy-1)*tile_height))
    surf.blit(load_tile(V_XW_M), ((cx-offset)*tile_width, cy *tile_height))
    surf.blit(load_tile(V_XW_R), ((cx-offset)*tile_width, (cy+1)*tile_height))

    surf.blit(load_tile(V_XW_L), ((cx+offset)*tile_width, (cy-1)*tile_height))
    surf.blit(load_tile(V_XW_M), ((cx+offset)*tile_width, cy *tile_height))
    surf.blit(load_tile(V_XW_R), ((cx+offset)*tile_width, (cy+1)*tile_height))

paint_h_road(background, cy, 0, gx-1)
paint_v_road(background, cx, 0, gy-1)
paint_crosswalks_around(background, cx, cy, offset = 2)

#change the 3x3 middle to be all solid

center_id = 407
ring_id = 441

def put_tile(surf, tid, tx, ty):
    surf.blit(load_tile(tid), (tx *tile_width, ty*tile_height))

def set_center_3x3(surf, cx, cy):
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            tid = center_id if (dx == 0 and dy == 0) else ring_id
            put_tile(surf, tid, cx+dx, cy+dy)

gx, g =WIDTH//tile_width, HEIGHT//tile_height
cx,cy = gx//2, gy//2
set_center_3x3(background, cx, cy)


#blit the background to our screen
screen.blit(background, (0,0))
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