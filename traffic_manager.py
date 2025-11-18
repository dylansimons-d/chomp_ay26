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

    @staticmethod
    def _lane_of(c):
        return 'E' if c.vx> 0 else 'W' if c.vx<0 else 'S' if c.vy>0 else 'N'
    
    @staticmethod
    def _axis(c):
        return 'EW' if abs(c.vx) >= abs(c.vy) else 'NS'
    
    @staticmethod
    def _dir_sign(c):
        # +1 if E or S, -1 if W or N; also return axis
        if abs(c.vx) >= abs(c.vy):
            return (1 if c.vx > 0 else -1), 'EW'
        else:
            return (1 if c.vy > 0 else -1), 'NS'

    @staticmethod
    def _front_pos(c):
        half = c.w*0.5 if abs(c.vx)>= abs(c.vy) else c.h * 0.5
        return (c.x +half) if c.vx>0 else (c.x -half) if c.vx< 0 else \
               (c.y +half) if c.vy>0 else (c.y -half) 
    
    @staticmethod
    def _rear_pos(c):
        half = c.w*0.5 if abs(c.vx)>=abs(c.vy) else c.h*0.5
        return (c.x - half) if c.vx>0 else (c.x + half) if c.vx<0 else \
               (c.y - half) if c.vy>0 else (c.y + half)
    
    def should_que(self, car, cars, gap_px, dt= 0, lane_tol= 2.5):
        sign, axis = self._dir_sign(car)

        best_dist = None
        leader = None
        if axis == 'EW':
            lane_y = car.y
            my_pos = car.x
            for other in cars:
                if other is car: 
                    continue
                if self._axis(other) != 'EW':
                    continue
                # same lane line?
                if abs(other.y - lane_y) > lane_tol:
                    continue
                # ahead in my travel direction?
                if sign > 0 and other.x <= my_pos:
                    continue
                if sign < 0 and other.x >= my_pos:
                    continue
                dist = abs(other.x - my_pos)
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    leader = other
        else:  # 'NS'
            lane_x = car.x
            my_pos = car.y
            for other in cars:
                if other is car:
                    continue
                if self._axis(other) != 'NS':
                    continue
                if abs(other.x - lane_x) > lane_tol:
                    continue
                if sign > 0 and other.y <= my_pos:
                    continue
                if sign < 0 and other.y >= my_pos:
                    continue
                dist = abs(other.y - my_pos)
                if best_dist is None or dist < best_dist:
                    best_dist = dist
                    leader = other

        if leader is None:
            return False  # no one ahead → free to go

        # Project MY next front position this frame.
        if axis == 'EW':
            next_front = (car.x + car.vx * dt) + (car.w * 0.5 if sign > 0 else -car.w * 0.5)
            leader_rear = self._rear_pos(leader)
            if sign > 0:
                return next_front > (leader_rear - gap_px)
            else:
                return next_front < (leader_rear + gap_px)
        else:  # 'NS'
            next_front = (car.y + car.vy * dt) + (car.h * 0.5 if sign > 0 else -car.h * 0.5)
            leader_rear = self._rear_pos(leader)
            if sign > 0:
                return next_front > (leader_rear - gap_px)
            else:
                return next_front < (leader_rear + gap_px)

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

class IntersectionCrashDetector:
    def __init__(self, x_mid, y_mid, tile_w, tile_h, scale = 1.05):
        w = int(tile_w * scale); h = int(tile_h * scale)
        self.zone = pygame.Rect(int(x_mid - w//2), int(y_mid - h//2), w, h)
        self.crash_sound = pygame.mixer.Sound('Assets\Audio\impactPunch_heavy_004.ogg')
        

    @staticmethod
    def _axis_of(c):
        return'EW' if abs(c.vx) >= abs(c.vy) else 'NS'

    @staticmethod
    def _rect(c):
        return pygame.Rect(int(c.x - c.w/2), int(c.y - c.h/2), int(c.w), int(c.h))
    
    def check(self, cars):
        inside = []
        for c in cars:
            r = self._rect(c)
            if r.colliderect(self.zone):
                inside.append((c, r))
        for i in range(len(inside)):
            ci, ri = inside[i]
            axi = self._axis_of(ci)
            for j in range(i+1, len(inside)):
                cj, rj = inside[j]
                if axi != self._axis_of(cj) and ri.colliderect(rj):
                    return True, cj, cj
                self.crash_sound.play()
        return False, None, None
        
    def debug_draw(self, screen, color=(255,0,255)):
        pygame.draw.ract(screen,color, self.zone, 2)
