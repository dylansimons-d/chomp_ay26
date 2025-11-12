import pygame
from util_params import *
from util_background import *
from car import *
from traffic_lights import *
from traffic_manager import *


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

background = build_background()
#grid and pixel locations
grid_w, grid_h, cx, cy, tile_w, tile_h = grid_info()
x_mid = cx * tile_w + tile_w *0.5 * tile_w
y_mid = cy * tile_h + tile_h * 0.5 * tile_h

# light cycle
lights = Lights(cycle_time = 8.0)
should_stop = make_should_stop(cx, cy, tile_w, tile_h, cross_offset = 2, nudge = 0.15)

#traffic
spawner = Spawner(cx, cy, tile_w, tile_h, WIDTH, HEIGHT)
cars = []
spawner.seed(cars, per_lane =1)

#score
score = 0
font = pygame.font.SysFont("consolas", 20)

#################### TESTING ZONE ##########################



#############################################################


while running:
    #clock
    dt = clock.tick(60) / 1000

    #press space to control lights 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lights.toggle()

    lights.update(dt) 
    spawner.step_spawn(cars, dt)   

    #loop for cars if not at light
    for c in cars:
        if not should_stop(c, lights.phase,dt):
            c.update(dt)
        if c.offscreen(WIDTH,HEIGHT):
            score += 1
            spawner.respawn_same_lane(c)
            
    # RENDER YOUR GAME HERE
    screen.blit(background, (0,0))
    for c in cars:c.draw(screen)
    score_surf = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_surf, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    #clock.tick(60)  # limits FPS to 60

pygame.quit()