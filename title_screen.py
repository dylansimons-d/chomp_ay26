import pygame
import math

def run_title(screen, clock, WIDTH, HEIGHT, background=None):
    big = pygame.font.SysFont("consolas", 48, bold =True)
    mid = pygame.font.SysFont("consolas", 24)
    small =  pygame.font.SysFont("consolas", 18)

    t = 0
    running_title = True
    while running_title:
        dt = clock.tick(60) / 1000
        t += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # quick fade-out
                    for a in range(0, 180, 9):
                        # redraw frame
                        if background:
                            screen.blit(background, (0,0))
                        else:
                            screen.fill((20, 24, 28))
                        
                        _draw_title_contents(screen, WIDTH, HEIGHT, big, mid, small, t)

                        fade = pygame.Surface((WIDTH, HEIGHT))
                        fade.set_alpha(a)
                        fade.fill((0,0,0))
                        screen.blit(fade, (0,0))
                        pygame.display.flip()
                        clock.tick(120)
                    return True
        if background:
            screen.blit(background,(0,0))
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            shade.fill ((0,0,0,120))
            screen.blit(shade, (0,0))
        else:
            screen.fill((20, 24, 28))
        
        _draw_title_contents(screen, WIDTH, HEIGHT, big, mid, small, t)
        pygame.display.flip()

def _draw_title_contents(screen, W, H, big, small, mid, t):
    title = big.render("Traffic Manager", True, (255, 255, 255))
    screen.blit(title, (W//2 - title.get_width()//2, H//3 - 30))

    car_w, car_h = 90, 36
    x = (W//2 - car_w//2) + int(40 * math.sin(t*2.2))
    y = H//3 + 40
    pygame.draw.rect(screen, (240, 160, 30), pygame.Rect(x, y, car_w, car_h), border_radius=8)
    pygame.draw.circle(screen, (30,30,30), (x+18, y+car_h), 8)
    pygame.draw.circle(screen, (30,30,30), (x+car_w-18, y+car_h), 8)

    lines = [
        "Controls:",
        "SPACE – toggle lights",
        ]
    y0 = y + 70
    for i, txt in enumerate(lines):
        surf = mid.render(txt, True, (220, 220, 220))
        screen.blit(surf, (W//2 - surf.get_width()//2, y0 + i*26))

    # blinking press-to-start
    blink_alpha = 160 + int(95 * (0.5 + 0.5*math.sin(t*6.0)))
    press = small.render("Press SPACE to start", True, (255,255,255))
    press_surf = pygame.Surface(press.get_size(), pygame.SRCALPHA)
    press_surf.fill((0,0,0,0))
    press_surf.blit(press, (0,0))
    # draw with simulated alpha by tinting a bg pill
    pill = pygame.Surface((press.get_width()+24, press.get_height()+12), pygame.SRCALPHA)
    pill.fill((0,0,0, blink_alpha))
    screen.blit(pill, (W//2 - pill.get_width()//2, H - 120))
    screen.blit(press, (W//2 - press.get_width()//2, H - 120 + 6))

