import pygame
from util_params import *
from random import randint

SIREN_PATH = "Assets\siren.wav"

_siren_sound = None
def _get_siren():
    global _siren_sound
    if _siren_sound is None:
        try:
            _siren_sound = pygame.mixer.Sound(SIREN_PATH)
            _siren_sound.set_volume(0.4)  # default volume
        except Exception:
            _siren_sound = None
    return _siren_sound

#class car
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
        
    #update location of cars   
    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy *dt
        # update the rect
        self.rect.center = (int(self.x), int(self.y))


    #create a rectangle for car
    def draw(self, surf):
        rect = pygame.Rect(int(self.x - self.w/2), int(self.y -self.h/2), int(self.w), int(self.h))
        pygame.draw.rect(surf, self.color, rect, border_radius = 6)

    #help it loop around/ reset it
    def offscreen(self, W, H):
        return self.x < -60 or self.x > W+60 or self.y < -60 or self.y > H+60
    
    #reset
    def reset(self):
        self.x , self.y = self.start
        self.rect.center = (int(self.x), int(self.y))

#building the car
def build_car(tile_w, tile_h, cx, cy, WIDTH, HEIGHT, speed = 160):
    #put cars on the right side of the roads
    x_mid = cx * tile_w + tile_w * 0.5
    y_mid = cy * tile_h  + tile_h *0.5

    lane_off = tile_w * 0.7
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
    #return the car
    return [
        Car(lanes['E']['x'], lanes['E']['y'], lanes['E']['vx'], lanes['E']['vy'], car_len, car_wid, (240, 160, 30)),
        Car(lanes['W']['x'], lanes['W']['y'], lanes['W']['vx'], lanes['W']['vy'], car_len, car_wid, (230, 90, 90)),
        Car(lanes['S']['x'], lanes['S']['y'], lanes['S']['vx'], lanes['S']['vy'], car_wid, car_len, (80, 200, 120)),
        Car(lanes['N']['x'], lanes['N']['y'], lanes['N']['vx'], lanes['N']['vy'], car_wid, car_len, (80, 120, 240))
    ]

# --- Player-controlled emergency vehicle ---
class Emergency(Car):
    def __init__(self, x, y, vx, vy, w, h, color=(230, 230, 230)):
        super().__init__(x, y, vx, vy, w, h, color)
        self.siren = False
        self.flash_t = 0.0
        self.base_speed = 220
        self.boost_mult = 1.5  # hold SHIFT for boost
        self._chan = None

    def control(self, keys, dt):
        # Arrow keys or WASD
        up    = keys[pygame.K_UP] or keys[pygame.K_w]
        down  = keys[pygame.K_DOWN] or keys[pygame.K_s]
        left  = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        boost = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        spd = self.base_speed * (self.boost_mult if boost else 1.0)

        # 4-way control
        self.vx = (right - left) * spd
        self.vy = (down  - up)   * spd

        # update position using normal Car.update(dt)
        super().update(dt)

    def toggle_siren(self):
        if self.siren:
            self.stop_siren()
        else:
            self.start_siren()
    
    def start_siren(self):
        snd = _get_siren()
        if snd is None:  # file missing or load failed
            self.siren = False
            return
        if self._chan is None or not self._chan.get_busy():
            self._chan = snd.play(loops=-1)
        self.siren = True

    def stop_siren(self):
        if self._chan is not None:
            self._chan.stop()
            self._chan = None
        self.siren = False

    def draw(self, surf):
        # body
        rect = pygame.Rect(int(self.x - self.w/2), int(self.y - self.h/2), int(self.w), int(self.h))
        pygame.draw.rect(surf, self.color, rect, border_radius=6)

        # flashing lightbar (top of vehicle)
        self.flash_t += 0.016  # approx per-frame; looks fine
        phase = (int(self.flash_t * 8) % 2)  # toggles ~8 Hz
        left_col  = (220, 50, 50) if phase == 0 else (50, 120, 255)
        right_col = (50, 120, 255) if phase == 0 else (220, 50, 50)

        lw = int(self.w * 0.18); lh = int(self.h * 0.18)
        # two little squares centered on roof
        lx = int(self.x - lw - 2); rx = int(self.x + 2)
        ly = int(self.y - self.h/2 + 4)
        pygame.draw.rect(surf, left_col,  pygame.Rect(lx, ly, lw, lh), border_radius=3)
        pygame.draw.rect(surf, right_col, pygame.Rect(rx, ly, lw, lh), border_radius=3)




