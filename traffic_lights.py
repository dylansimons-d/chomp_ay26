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

        
