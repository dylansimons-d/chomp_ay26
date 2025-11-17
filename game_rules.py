import pygame

class IntersectionCrashDetector:
    """Detect perpendicular-axis crashes inside the intersection."""
    def __init__(self, x_mid, y_mid, tile_w, tile_h, scale=1.05):
        w = int(tile_w * scale); h = int(tile_h * scale)
        self.zone = pygame.Rect(int(x_mid - w//2), int(y_mid - h//2), w, h)

    @staticmethod
    def _axis_of(c):  # 'EW' for horizontal, 'NS' for vertical
        return 'EW' if abs(c.vx) >= abs(c.vy) else 'NS'

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
                    return True, ci, cj
        return False, None, None

    def debug_draw(self, screen, color=(255, 0, 255)):
        pygame.draw.rect(screen, color, self.zone, 2)


class QueueDefeat:
    """
    Lose if too many cars are queued behind one approach (E/W/N/S).
    Counts cars whose FRONT bumper is still before the stop line,
    aligned to the lane, within a counting window.
    """
    def __init__(self, cx, cy, tile_w, tile_h,
                 lane_dx, lane_dy,
                 cross_offset=2, slack=0.15,
                 lane_tol=6.0, window_tiles=20, limit=10):
        self.tile_w = tile_w; self.tile_h = tile_h
        self.cx = cx; self.cy = cy
        self.dx = lane_dx; self.dy = lane_dy
        self.slackx = slack * tile_w; self.slacky = slack * tile_h
        self.lane_tol = lane_tol; self.limit = limit

        # stop lines (pixels)
        self.stop_e_x = (cx - cross_offset) * tile_w
        self.stop_w_x = (cx + cross_offset) * tile_w
        self.stop_s_y = (cy - cross_offset) * tile_h
        self.stop_n_y = (cy + cross_offset) * tile_h

        # counting window behind each line (pixels)
        self.window_x = window_tiles * tile_w
        self.window_y = window_tiles * tile_h

        # lane centerlines (pixels)
        self.y_top_lane    = cy * tile_h + 0.5 * tile_h - self.dy   # EW eastbound
        self.y_bottom_lane = cy * tile_h + 0.5 * tile_h + self.dy   # EW westbound
        self.x_left_lane   = cx * tile_w + 0.5 * tile_w - self.dx   # NS northbound
        self.x_right_lane  = cx * tile_w + 0.5 * tile_w + self.dx   # NS southbound

    @staticmethod
    def _axis(c): return 'EW' if abs(c.vx) >= abs(c.vy) else 'NS'
    def _front_x(self, c): return c.x + (c.w*0.5 if c.vx>0 else -c.w*0.5)
    def _front_y(self, c): return c.y + (c.h*0.5 if c.vy>0 else -c.h*0.5)

    def check(self, cars):
        counts = {'E':0,'W':0,'N':0,'S':0}
        for c in cars:
            ax = self._axis(c)
            if ax == 'EW':
                if abs(c.y - self.y_top_lane) <= self.lane_tol and c.vx > 0:
                    fx = self._front_x(c)
                    if fx < self.stop_e_x - self.slackx and (self.stop_e_x - fx) <= self.window_x:
                        counts['E'] += 1
                elif abs(c.y - self.y_bottom_lane) <= self.lane_tol and c.vx < 0:
                    fx = self._front_x(c)
                    if fx > self.stop_w_x + self.slackx and (fx - self.stop_w_x) <= self.window_x:
                        counts['W'] += 1
            else:
                # SOUTHBOUND (vy>0) on LEFT lane (x_mid - dx)
                if c.vy > 0 and abs(c.x - self.x_left_lane) <= self.lane_tol:
                    fy = self._front_y(c)
                    # approaching S line from above; queued if front is BEFORE the line
                    if fy < self.stop_s_y - self.slacky and (self.stop_s_y - fy) <= self.window_y:
                        counts['S'] += 1

                # NORTHBOUND (vy<0) on RIGHT lane (x_mid + dx)
                elif c.vy < 0 and abs(c.x - self.x_right_lane) <= self.lane_tol:
                    fy = self._front_y(c)
                    # approaching N line from below; queued if front is BEFORE the line
                    if fy > self.stop_n_y + self.slacky and (fy - self.stop_n_y) <= self.window_y:
                        counts['N'] += 1


        for k in ('E','W','N','S'):
            if counts[k] >= self.limit:
                return True, k, counts[k]
        return False, None, 0