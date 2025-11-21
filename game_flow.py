import pygame
from util_params import WIDTH, HEIGHT
from util_background import build_background, grid_info
from traffic_lights import Lights, make_should_stop
from traffic_manager import Spawner
from game_rules import IntersectionCrashDetector, QueueDefeat

def start_round(limit_queue=10, cycle_time=8.0):
    """Build a fresh round and return all state objects + score."""
    background = build_background()

    grid_w, grid_h, cx, cy, tile_w, tile_h = grid_info()
    x_mid = cx * tile_w + 0.5 * tile_w
    y_mid = cy * tile_h + 0.5 * tile_h

    lights = Lights(cycle_time=cycle_time)
    should_stop = make_should_stop(cx, cy, tile_w, tile_h, cross_offset=2, nudge=0.15)
    spawner = Spawner(cx, cy, tile_w, tile_h, WIDTH, HEIGHT)
    cars = []
    spawner.seed(cars, per_lane=1)

    crash = IntersectionCrashDetector(x_mid, y_mid, tile_w, tile_h, scale=1.05)
    queue_loss = QueueDefeat(cx, cy, tile_w, tile_h, spawner.dx, spawner.dy, limit=limit_queue)

    score = 0
    return (background, cx, cy, tile_w, tile_h, x_mid, y_mid,
            lights, should_stop, spawner, cars, crash, queue_loss, score)

def game_over_overlay(screen, msg, background):
    """Show overlay and wait for R=restart or ESC/close=quit."""
    font_big = pygame.font.SysFont("consolas", 36, bold=True)
    font_small = pygame.font.SysFont("consolas", 22)
    clock = pygame.time.Clock()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:         return "quit"
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:  return "quit"
                if e.key == pygame.K_r:       return "restart"

        screen.blit(background, (0, 0))
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 170))
        screen.blit(ov, (0, 0))

        txt = font_big.render(msg, True, (255, 255, 255))
        sub = font_small.render("Press R to restart  •  ESC to quit", True, (230, 230, 230))
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 40))
        screen.blit(sub, (WIDTH//2 - sub.get_width()//2, HEIGHT//2 + 10))

        pygame.display.flip()
        clock.tick(60)