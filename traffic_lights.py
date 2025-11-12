import pygame
from util_background import *

class Lights():
    def __init__(self, cycle_time = 8):
        #east and west green
        self.phase = 'EW'
        self.auto = False
        self.timer = 0
        self.cycle_time = cycle_time

    def toggle(self):
        self.phase = 'NS' if self.phase == 'EW' else 'EW'

    def update(self, dt):
        if self.auto:
            self.timer += dt
            if self.timer >= self.cycle_time:
                self.timer = 0
                self.toggle()
    
    def draw(self, screen, x_mid, y_mid, tile_w):
        r = int(tile_w * 0.25)
        off = tile_w * 1.1
        green = (80, 220, 80)
        red = (220, 60, 60)
        col = green if self.phase =='EW' else red
        for dx in (-off, +off):
            for dy in (-off, +off):
                pygame.draw.circle(screen, col, (int(x_mid + dx), int(y_mid + dy)), r)

def make_should_stop(cx, cy, tile_w, tile_h, cross_offset=2, nudge=0.15):
    
    stop_e = (cx - cross_offset) * tile_w
    stop_w = (cx + cross_offset) * tile_w
    stop_s = (cy - cross_offset) * tile_h
    stop_n = (cy + cross_offset) * tile_h
    nudge_x = nudge * tile_w
    nudge_y = nudge * tile_h

    def half_along(c):
        return (c.w * 0.5) if abs(c.vx) >= abs(c.vy) else (c.h * 0.5)

    def should_stop(car, phase, dt):
        horiz = abs(car.vx) >= abs(car.vy)   # my lane axis
        my_axis = 'EW' if horiz else 'NS'
        if phase == my_axis:
            return False  # I'm green

        # predict next position (look-ahead)
        nx = car.x + car.vx * dt
        ny = car.y + car.vy * dt
        half = half_along(car)

        if horiz:
            if car.vx > 0:   # Eastbound — stop before STOP_E
                return (nx + half) >= (stop_e - nudge_x)
            else:            # Westbound — stop after STOP_W
                return (nx - half) <= (stop_w + nudge_x)
        else:
            if car.vy > 0:   # Southbound — stop before STOP_S
                return (ny + half) >= (stop_s - nudge_y)
            else:            # Northbound — stop after STOP_N
                return (ny - half) <= (stop_n + nudge_y)

    return should_stop
        
