import pygame
from random import randint
from car import Car

class Spawner:
    def __init__(self, cx, cy, tile_w, tile_h, W, H, lane_spacing_x =0.5, lane_spacing_y=0.5, car_len=0.90, car_wid=0.46):
        self.W = W
        self.H = H
        self.tile_w = tile_w
        self.tile_h = tile_h

        x_mid = cx * tile_w + tile_w * 0.5
        y_mid = cy * tile_h  + tile_h *0.5

        self.dx = lane_spacing_x * tile_w
        self.dy = lane_spacing_y * tile_h

        self.car_l = car_len *tile_w
        self.car_w = car_wid * tile_w

        self.lane_def = {
            'E': {'x': -40,'y': y_mid - self.dy, 'vx': +1, 'vy': 0},
            'W': {'x': W + 40,'y': y_mid + self.dy, 'vx': -1, 'vy': 0},
            'S': {'x': x_mid - self.dx, 'y': -40,'vx': 0,  'vy': +1},
            'N': {'x': x_mid + self.dx, 'y': H + 40,'vx': 0,  'vy': -1},
        }

        self.spawn_cd = {k: 0 for k in 'EWNS'}
        for k in self.spawn_cd: self._reset_timer(k)

    def _reset_timer(self, lane_key):
        self.spawn_cd[lane_key] = randint(50,150) / 25

    def _lane_of(self, c):
        return 'E' if c.vx> 0 else 'W' if c.vx<0 else 'S' if c.vy>0 else 'N'
    
    def _front_pos(c):
        half = c.w*0.5 if abs(c.vx)>= abs(c.vy) else c.h * 0.5
        return (c.x +half) if c.vx>0 else (c.x -half) if c.vx< 0 else \
               (c.y +half) if c.vy>0 else (c.y -half) 
    
    def _rear_pos(c):
        half = c.w*0.5 if abs(c.vx)>=abs(c.vy) else c.h*0.5
        return (c.x - half) if c.vx>0 else (c.x + half) if c.vx<0 else \
               (c.y - half) if c.vy>0 else (c.y + half)

    def _entrance_clear(self, lane_key, cars, need_len):
        sx, sy = self.lane_def[lane_key]['x'], self.lane_def[lane_key]['y']
        horiz = lane_key in ('E', 'W')
        for c in cars:
            if horiz and abs(c.y -sy) < 2 and abs(c.x - sx) <need_len:
                return False
            if not horiz and abs(c.x -sx) < 2 and abs(c.y- sy) <need_len:
                return False
        return True
    
    def _new_car(self, lane_key, base_speed = 160):
        d = self.lane_def[lane_key]
        spd = randint (140, 180)
        vx, vy = d['vx']* spd, d['vy']* spd

        if lane_key in ('E', 'W'):
            w,h = self.car_l, self.car_w
        else:
            w, h = self.car_w, self.car_l
        color = (randint(80, 240), randint (80, 240), randint(80,240))
        return Car(d['x'], d['y'], vx, vy, w, h, color)
    
    def seed(self, cars, per_lane=1):
        for _ in range(per_lane):
            for k in 'EWNS':
                cars.append(self._new_car(k))

    def step_spawn(self, cars, dt):
        for k in 'EWNS':
            self.spawn_cd[k] -= dt
            if self.spawn_cd[k] <= 0.0:
                nc = self._new_car(k)
                need = 1.6 * (nc.w if abs(nc.vx)>=abs(nc.vy) else nc.h)
                if self._entrance_clear(k, cars, need):
                    cars.append(nc)
                self._reset_timer(k)

    def respawn_same_lane(self, car):
        k = self._lane_of(car)
        nc = self._new_car(k)
        car.x, car.y, car.vx, car.vy = nc.x, nc.y, nc.vx, nc.vy
        car.w, car.h, car.color = nc.w, nc.h, nc.color


