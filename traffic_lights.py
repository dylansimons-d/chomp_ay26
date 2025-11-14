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
    
    def draw(self, screen, x_mid, y_mid, tile_w, lane_offset_x=None, lane_offset_y=None):
        r   = int(tile_w * 0.22)
        off = tile_w * 1.30          # distance from center to the far-side mast

        # If you already use LANE_SPACING_X/Y elsewhere, pass them in here.
        lx = lane_offset_x if lane_offset_x is not None else 0.28 * tile_w  # N/S lanes offset (x)
        ly = lane_offset_y if lane_offset_y is not None else 0.28 * tile_w  # E/W lanes offset (y)

        green = (80, 220, 80)
        red   = (220, 60, 60)

        # Colors by phase
        col_EW = green if self.phase == 'EW' else red
        col_NS = green if self.phase == 'NS' else red

        # BACKING box so lights pop over map
        box_w = box_h = int(tile_w * 0.55)

        def draw_head(px, py, color):
            back = pygame.Rect(px - box_w//2, py - box_h//2, box_w, box_h)
            pygame.draw.rect(screen, (0,0,0), back, border_radius=6)
            pygame.draw.circle(screen, color, (px, py), r)
            pygame.draw.circle(screen, (20,20,20), (px, py), r, width=2)

        # --- E/W approaches: far side on ±X, duplicate at y_mid ± ly ---
        # Eastbound looks to the east side (x_mid + off)
        ex = int(x_mid + off)
        draw_head(ex, int(y_mid - ly), col_EW)   # upper EW lane
        draw_head(ex, int(y_mid + ly), col_EW)   # lower EW lane

        # Westbound looks to the west side (x_mid - off)
        wx = int(x_mid - off)
        draw_head(wx, int(y_mid - ly), col_EW)
        draw_head(wx, int(y_mid + ly), col_EW)

        # --- N/S approaches: far side on ±Y, duplicate at x_mid ± lx ---
        # Northbound looks to the north side (y_mid - off)
        ny = int(y_mid - off)
        draw_head(int(x_mid - lx), ny, col_NS)   # left NS lane
        draw_head(int(x_mid + lx), ny, col_NS)   # right NS lane

        # Southbound looks to the south side (y_mid + off)
        sy = int(y_mid + off)
        draw_head(int(x_mid - lx), sy, col_NS)
        draw_head(int(x_mid + lx), sy, col_NS)

def make_should_stop(cx, cy, tile_w, tile_h, cross_offset=2, nudge=0.15):
    
    stop_e_x = (cx - cross_offset) * tile_w
    stop_w_x = (cx + cross_offset) * tile_w
    stop_s_y = (cy - cross_offset) * tile_h
    stop_n_y = (cy + cross_offset) * tile_h
    nudgex = nudge * tile_w
    nudgey = nudge * tile_h

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
            sign = 1 if car.vx > 0 else -1
            front_now  = car.x + sign * (car.w * 0.5)
            front_next = front_now + car.vx * dt
            if sign > 0:  # E → approaching stop_e_x from left
                if front_now >= stop_e_x - nudgex:   # already past → never stop
                    return False
                return front_next >= stop_e_x - nudgex
            else:         # W → approaching stop_w_x from right
                if front_now <= stop_w_x + nudgex:
                    return False
                return front_next <= stop_w_x + nudgex
        else:
            sign = 1 if car.vy > 0 else -1
            front_now  = car.y + sign * (car.h * 0.5)
            front_next = front_now + car.vy * dt
            if sign > 0:  # S → approaching stop_s_y from above
                if front_now >= stop_s_y - nudgey:
                    return False
                return front_next >= stop_s_y - nudgey
            else:         # N → approaching stop_n_y from below
                if front_now <= stop_n_y + nudgey:
                    return False
                return front_next <= stop_n_y + nudgey

    return should_stop
        
