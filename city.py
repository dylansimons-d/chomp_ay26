import pygame
from util_params import *
from util_background import *
from car import *
from traffic_lights import *
from traffic_manager import *
from title_screen import run_title
from game_rules import *
from game_flow import *

# pygame setup
pygame.mixer.init(frequency=44100, size = -16, channels = 2, buffer = 512)
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
queue_loss = QueueDefeat(cx, cy, tile_w, tile_h, spawner.dx, spawner.dy, limit=10)

cars = []
spawner.seed(cars, per_lane =1)

lane_spacing_x = spawner.dx
lane_spacing_y = spawner.dy

#score
score = 0
font = pygame.font.SysFont("consolas", 20)
app_running = True

#################### TESTING ZONE ##########################




#############################################################


while app_running:
    (background, cx, cy, tile_w, tile_h, x_mid, y_mid,
     lights, should_stop, spawner, cars, crash, queue_loss, score) = start_round(limit_queue=10)

    lane_spacing_x, lane_spacing_y = spawner.dx, spawner.dy
    follow_gap = 0.6 * tile_w

    player = None
    next_ev_score = 51  # first threshold

    def spawn_emergency(x_mid, y_mid, lane_dx, tile_w):
        w = 0.50 * tile_w
        h = 0.90 * tile_w 
        # Import Emergency if not already: from car import Emergency
        return Emergency(
            x = x_mid + lane_dx,   # align with northbound lane
            y = HEIGHT - (h*0.6),
            vx = 0, vy = -220,
            w = w, h=h
        )

    round_running = True
    while round_running:
        dt = clock.tick(60) / 1000
        keys = pygame.key.get_pressed()
        #control/ update the emergency vehicle
        if player is not None:
            player.control(keys, dt)
            if player.offscreen(WIDTH, HEIGHT):
                player.stop_siren()
                player = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                round_running = False
                app_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lights.toggle()
                elif event.key == pygame.K_f and player is not None:
                    player.toggle_siren()

        if not app_running:
            break

        lights.update(dt)
        spawner.step_spawn(cars, dt)

        for c in cars:
            stop_red   = should_stop(c, lights.phase, dt)
            stop_que = spawner.should_que(c, cars, gap_px=follow_gap, dt=dt)  
            if not (stop_red or stop_que):
                c.update(dt)
            if c.offscreen(WIDTH, HEIGHT):
                score += 1
                spawner.respawn_same_lane(c)
            if player is None and score >= next_ev_score:
                player = spawn_emergency(x_mid, y_mid, lane_spacing_x, tile_w)
                player.start_siren()
                next_ev_score += 51

        # gridlock
        lost, approach, count = queue_loss.check(cars)
        if lost:
            choice = game_over_overlay(screen, f"GRIDLOCK on {approach}: {count} cars", background)
            if choice == "restart":
                round_running = False
                continue
            app_running = False
            round_running = False
            continue

        # crash
        crashed, a, b = crash.check(cars)
        if crashed:
            choice = game_over_overlay(screen, "CRASH!  Game Over", background)
            if choice == "restart":
                round_running = False
                continue
            app_running = False
            round_running = False
            continue

        # draw
        screen.blit(background, (0,0))
        lights.draw(screen, x_mid, y_mid, tile_w,
                    lane_offset_x=lane_spacing_x, lane_offset_y=lane_spacing_y)
        for c in cars: c.draw(screen)
        if player is not None: 
            player.draw(screen)
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
        pygame.display.flip()

pygame.quit()