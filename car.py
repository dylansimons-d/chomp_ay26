import pygame
from util_params import *

class Car():
    def __init__(self, x, y, vx, vy, w, h, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.color = color
        self.rect = pygame.Rect(0,0, int(w), int(h))
        self.rect.center = (int(x), int(y))
        self.start = (x,y)
        
    #update location    
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy *dt
        # update the rect
        self.rect.center = (int(self.x), int(self.y))


    #create a rectangle
    def draw(self, surf):
        rect = pygame.Rect(int(self.x - self.w/2), int(self.y -self.h/2), int(self.w), int(self.h))
        pygame.draw.rect(surf, self.color, rect, border_radius = 6)

    def offscreen(self, W, H):
        return self.x < -60 or self.x > W+60 or self.y < -60 or self.y > H+60
    
    def reset(self):
        self.x , self.y = self.start
        self.rect.center = (int(self.x), int(self.y))

def build_car(tile_w, tile_h, cx, cy, WIDTH, HEIGHT, speed = 160):
    #put cars on the right side of the roads
    x_mid = cx * tile_w + tile_w * 0.5
    y_mid = cy * tile_h  + tile_h *0.5

    lane_off = tile_w * 0.25
    car_len = tile_w * 0.9
    car_wid = tile_w * 0.5

    #make the lanes
    lanes = {
        #left to right
        'E' : {'x': -40, 'y':y_mid - lane_off, 'vx': + speed, 'vy':0},
        #right to left
        'W': {'x': WIDTH + 40, 'y':y_mid + lane_off, 'vx': - speed, 'vy':0},
        #top to bottom
        'S': {'x': x_mid - lane_off, 'y': -40, 'vx': 0, 'vy': +speed},
        #bottom to top
        'N': {'x': x_mid + lane_off, 'y':HEIGHT + 40, 'vx': 0, 'vy': -speed}
    }

    return [
        Car(lanes['E']['x'], lanes['E']['y'], lanes['E']['vx'], lanes['E']['vy'], car_len, car_wid, (240, 160, 30)),
        Car(lanes['W']['x'], lanes['W']['y'], lanes['W']['vx'], lanes['W']['vy'], car_len, car_wid, (230, 90, 90)),
        Car(lanes['S']['x'], lanes['S']['y'], lanes['S']['vx'], lanes['S']['vy'], car_wid, car_len, (80, 200, 120)),
        Car(lanes['N']['x'], lanes['N']['y'], lanes['N']['vx'], lanes['N']['vy'], car_wid, car_len, (80, 120, 240))
    ]

        

