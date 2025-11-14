import pygame
from util_params import *
from util_background import *
from car import *
from traffic_lights import *
from traffic_manager import *
from title_screen import run_title

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
background = build_background()

start = run_title(screen, clock, WIDTH, HEIGHT, background=background)
if not start:
    pygame.quit()
    raise SystemExit

#grid and pixel locations
grid_w, grid_h, cx, cy, tile_w, tile_h = grid_info()
x_mid = cx * tile_w + 0.5 * tile_w
y_mid = cy * tile_h + 0.5 * tile_h

#crash
crash = IntersectionCrashDetector(x_mid, y_mid, tile_w, tile_h, scale=1.05)

#lights
lights = Lights(cycle_time = 8.0)
should_stop = make_should_stop(cx, cy, tile_w, tile_h, cross_offset = 2, nudge = 0.15)

#traffic
spawner = Spawner(cx, cy, tile_w, tile_h, WIDTH, HEIGHT)

cars = []
spawner.seed(cars, per_lane =1)

lane_spacing_x = spawner.dx
lane_spacing_y = spawner.dy

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
    follow_gap = 0.6 * tile_w
    #loop for cars if not at light
    for c in cars:
        stop_red = should_stop(c, lights.phase, dt)
        stop_queue = spawner.should_que(c, cars, gap_px=follow_gap, dt=dt)
        if not (stop_red or stop_queue):
            c.update(dt)
        if c.offscreen(WIDTH,HEIGHT):
            score += 1
            spawner.respawn_same_lane(c)

    #check crash
    crashed, a, b = crash.check(cars)
    if crashed:
        #quick game-over layover
        screen.blit(background, (0,0))
        lights.draw(screen, x_mid, y_mid, tile_w,
                    lane_offset_x=spawner.dx, lane_offset_y=spawner.dy)
        for c in cars: c.draw(screen)
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((160,0,0,140))
        screen.blit(ov, (0,0))
        msg = font.render("CRASH!  Game Over", True, (255,255,255))
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(5000)
        running = False
        continue

    # RENDER YOUR GAME HERE
    screen.blit(background, (0,0))
    lights.draw(screen, x_mid, y_mid, tile_w, lane_offset_x=lane_spacing_x, lane_offset_y=lane_spacing_y)
    for c in cars:
        c.draw(screen)
    score_surf = font.render(f"Score: {score}", True, (255,255,255))
    screen.blit(score_surf, (10, 10))

    # flip() the display to put your work on screen
    pygame.display.flip()

    #clock.tick(60)  # limits FPS to 60

pygame.quit()