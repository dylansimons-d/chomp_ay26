import pygame
from util_params import *
from util_background import *
from car import *
from traffic_lights import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

#score
score = 0
font = pygame.font.SysFont("consolas", 20)

#################### TESTING ZONE ##########################




#############################################################
#blit screen/ background
background = build_background()
screen.blit(background, (0,0))

#grid and pixel locations
grid_w, grid_h, cx, cy, tile_w, tile_h = grid_info()
x_mid = cx * tile_w + tile_w *0.5
y_mid = cy * tile_h + tile_h * 0.5

# light cycle
lights = Lights(cycle_time = 8.0)

#stop lines where cars should stop
cross_offset = 2
stop_e = (cx - cross_offset) * tile_w - 0.2 * tile_w
stop_w = (cx + cross_offset) * tile_w + 0.2 * tile_w
stop_s = (cy - cross_offset) * tile_h - 0.2 * tile_h
stop_n = (cy + cross_offset) * tile_h + 0.2 * tile_h

def should_stop(car, phase):
    if abs(car.vx) > abs(car.vy):
        axis = 'EW'
        at_line = car.x >= stop_e if car.vx > 0 else car.x <= stop_w 
    else: 
        axis = 'NS'
        at_line = car.x >= stop_s if car.vy > 0 else car.y <= stop_n
    return(phase != axis) and at_line


#build car
cars = build_car(tile_w, tile_h, cx, cy, WIDTH, HEIGHT, speed = 160)


while running:
    #clock
    dt = clock.tick(60) / 2000
    lights.update(dt)

    # RENDER YOUR GAME HERE
    screen.blit(background, (0,0))

    #loop for cars if not at light
    for c in cars:
        if not should_stop(c, lights.phase):
            c.update(dt)
        if c.offscreen(WIDTH,HEIGHT):
            score += 1
            c.reset()
        c.draw(screen)

    #press space to control lights t for auto
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                lights.toggle()
            

    lights.draw(screen, x_mid, y_mid, tile_w)

    score_surf = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_surf, (10, 10))
    # flip() the display to put your work on screen
    pygame.display.flip()

    #clock.tick(60)  # limits FPS to 60

pygame.quit()