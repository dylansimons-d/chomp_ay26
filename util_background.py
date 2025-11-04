import pygame
from util_params import WIDTH, HEIGHT


SCALE = 2  

# Tile IDs
GRASS = 28
H_T, H_M, H_B = 406, 433, 460           # horizontal road pieces
V_L, V_M, V_R = 461, 462, 463           # vertical road pieces
H_XW_T, H_XW_M, H_XW_B = 434, 435, 436  # horizontal crosswalks
V_XW_L, V_XW_M, V_XW_R = 405, 432, 459  # vertical crosswalks
CENTER_ID, RING_ID = 407, 441           # 3×3 center (407) + ring (441)

# Simple cache for scaled tiles
_tile_cache = {}

#helps with the tile numbers
def _load_scaled(idx, tw, th):
    key = (idx, tw, th)
    img = _tile_cache.get(key)
    if img is None:
        p = f"Assets/Tiles/tile_{idx:04}.png"
        raw = pygame.image.load(p).convert_alpha()
        img = pygame.transform.scale(raw, (tw, th))
        _tile_cache[key] = img
    return img

#measuring tiles and fitting them in place
def _measure_tile():
    grass = pygame.image.load("Assets/Tiles/tile_0028.png").convert_alpha()
    grass = pygame.transform.scale(grass, (grass.get_width()*SCALE, grass.get_height()*SCALE))
    return grass.get_width(), grass.get_height(), grass

#paint tiles
def _paint_grass(bg, tw, th):
    g = _load_scaled(GRASS, tw, th)
    for x in range(0, WIDTH, tw):
        for y in range(0, HEIGHT, th):
            bg.blit(g, (x, y))

def _paint_h_road(surf, cy, x0, x1, tw, th):
    for x in range(x0, x1+1):
        surf.blit(_load_scaled(H_T, tw, th), (x*tw, (cy-1)*th))
        surf.blit(_load_scaled(H_M, tw, th), (x*tw,  cy   *th))
        surf.blit(_load_scaled(H_B, tw, th), (x*tw, (cy+1)*th))

def _paint_v_road(surf, cx, y0, y1, tw, th):
    for y in range(y0, y1+1):
        surf.blit(_load_scaled(V_L, tw, th), ((cx-1)*tw, y*th))
        surf.blit(_load_scaled(V_M, tw, th), ( cx   *tw, y*th))
        surf.blit(_load_scaled(V_R, tw, th), ((cx+1)*tw, y*th))

def _paint_crosswalks(surf, cx, cy, tw, th, offset=2):
    # horizontal (north/south)
    surf.blit(_load_scaled(H_XW_T, tw, th), ((cx-1)*tw, (cy-offset)*th))
    surf.blit(_load_scaled(H_XW_M, tw, th), ( cx   *tw, (cy-offset)*th))
    surf.blit(_load_scaled(H_XW_B, tw, th), ((cx+1)*tw, (cy-offset)*th))
    surf.blit(_load_scaled(H_XW_T, tw, th), ((cx-1)*tw, (cy+offset)*th))
    surf.blit(_load_scaled(H_XW_M, tw, th), ( cx   *tw, (cy+offset)*th))
    surf.blit(_load_scaled(H_XW_B, tw, th), ((cx+1)*tw, (cy+offset)*th))
    # vertical (west/east)
    surf.blit(_load_scaled(V_XW_L, tw, th), ((cx-offset)*tw, (cy-1)*th))
    surf.blit(_load_scaled(V_XW_M, tw, th), ((cx-offset)*tw,  cy   *th))
    surf.blit(_load_scaled(V_XW_R, tw, th), ((cx-offset)*tw, (cy+1)*th))
    surf.blit(_load_scaled(V_XW_L, tw, th), ((cx+offset)*tw, (cy-1)*th))
    surf.blit(_load_scaled(V_XW_M, tw, th), ((cx+offset)*tw,  cy   *th))
    surf.blit(_load_scaled(V_XW_R, tw, th), ((cx+offset)*tw, (cy+1)*th))

#intersection tiles
def _set_center_3x3(surf, cx, cy, tw, th):
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            tid = CENTER_ID if (dx == 0 and dy == 0) else RING_ID
            surf.blit(_load_scaled(tid, tw, th), ((cx+dx)*tw, (cy+dy)*th))

#builds the background
def build_background():
    tw, th, _ = _measure_tile()
    gx, gy = WIDTH // tw, HEIGHT // th
    cx, cy = gx // 2, gy // 2

    bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    _paint_grass(bg, tw, th)
    _paint_h_road(bg, cy, 0, gx-1, tw, th)
    _paint_v_road(bg, cx, 0, gy,   tw, th)  # extend to bottom
    _paint_crosswalks(bg, cx, cy, tw, th, offset=2)
    _set_center_3x3(bg, cx, cy, tw, th)
    return bg


def grid_info():
    tw, th, _ = _measure_tile()
    gx, gy = WIDTH // tw, HEIGHT // th
    return gx, gy, gx//2, gy//2, tw, th