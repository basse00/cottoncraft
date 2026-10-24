"""CottonCraft's Prism icon (prism/cottoncraft.png): a pickaxe whose head is cotton bolls, and
"100% COTTON PICK". Drawn on a 64x64 grid, saved 4x (256 px).

Run: python3 .github/make-icon.py prism/cottoncraft.png  (needs Pillow)"""
from PIL import Image
import math, sys

N = 64
img = Image.new("RGBA", (N, N), (0, 0, 0, 0))
px = img.load()
def put(x, y, c):
    if 0 <= x < N and 0 <= y < N: px[x, y] = c

ORANGE, ORANGE_D = (226, 112, 38, 255), (150, 66, 18, 255)
WOOD, WOOD_L, WOOD_D = (150, 98, 52, 255), (196, 140, 80, 255), (84, 52, 26, 255)
BRACT, BRACT_D = (176, 112, 52, 255), (110, 64, 26, 255)
W, L, G, OUT = (255, 255, 255, 255), (226, 226, 230, 255), (186, 186, 194, 255), (110, 104, 112, 255)

# --- text, 3x5 font
F = {"1": ["010","110","010","010","111"], "0": ["111","101","101","101","111"],
     "%": ["101","001","010","100","101"], "C": ["111","100","100","100","111"],
     "O": ["111","101","101","101","111"], "T": ["111","010","010","010","010"],
     "N": ["101","111","111","101","101"], "P": ["111","101","111","100","100"],
     "I": ["111","010","010","010","111"], "K": ["101","101","110","101","101"], " ": ["000"]*5}
def text(s, y):
    w = len(s) * 4 - 1; x0 = (N - w) // 2
    for i, ch in enumerate(s):
        for r, row in enumerate(F[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    put(x0 + i*4 + c + 1, y + r + 1, ORANGE_D)   # shadow
    for i, ch in enumerate(s):
        for r, row in enumerate(F[ch]):
            for c, bit in enumerate(row):
                if bit == "1":
                    put(x0 + i*4 + c, y + r, ORANGE)
text("100% COTTON", 2)
text("PICK", 9)

# --- the head: a cotton branch bent like a Minecraft pickaxe's head, with
# a big boll in the middle and smaller ones towards the tips
ox, oy, R = 18, 52, 27                    # centre of the arc
P = lambda a, rr=R: (ox + rr*math.cos(math.radians(a)), oy + rr*math.sin(math.radians(a)))
bolls = [(-98, 4.9), (-72, 6.0), (-45, 7.6), (-18, 6.0), (8, 4.9)]

# --- handle: from bottom-left to the middle of the head
hx0, hy0, hx1, hy1 = 7, 60, 36, 31
def seg(x, y):
    vx, vy = hx1 - hx0, hy1 - hy0
    t = max(0, min(1, ((x-hx0)*vx + (y-hy0)*vy) / (vx*vx + vy*vy)))
    return math.hypot(x - hx0 - t*vx, y - hy0 - t*vy), ((x-hx0)*vy - (y-hy0)*vx) / math.hypot(vx, vy)
for y in range(N):
    for x in range(N):
        d, side = seg(x, y)
        if d <= 2.2:
            put(x, y, WOOD_D if d > 1.4 else WOOD_L if side < -0.3 else WOOD)

# --- the branch along the arc (brown, 2 px), under the bolls
for k in range(-104, 15):
    for dr in (-0.6, 0.6):
        x, y = P(k, R - 2 + dr); put(round(x), round(y), BRACT_D if dr > 0 else BRACT)

# --- each boll: three lobes on a star of brown husk leaves
lobes = []
for a, r in bolls:
    bx, by = P(a)
    ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))      # outwards
    # husk: leaves pointing out to the sides and back, under the lobes
    for sgn in (-1, 1):
        lx, ly = ux*0.2 - uy*sgn, uy*0.2 + ux*sgn
        for k in range(int(r) + 2):
            put(round(bx - ux*1.5 + lx*k), round(by - uy*1.5 + ly*k), BRACT_D if k > r - 1 else BRACT)
            put(round(bx - ux*2.3 + lx*k*0.8), round(by - uy*2.3 + ly*k*0.8), BRACT)
    for phi, f in ((-55, 0.62), (0, 0.66), (55, 0.62)):
        c, sn = math.cos(math.radians(phi)), math.sin(math.radians(phi))
        dx, dy = ux*c - uy*sn, uy*c + ux*sn
        lobes.append((bx + dx*r*0.42, by + dy*r*0.42, r*f))

inside = lambda x, y: any((x-a)**2 + (y-b)**2 <= r*r for a, b, r in lobes)
for y in range(N):
    for x in range(N):
        hits = [(a, b, r) for a, b, r in lobes if (x-a)**2 + (y-b)**2 <= r*r]
        if not hits:
            continue
        a, b, r = max(hits, key=lambda p: p[2]**2 - ((x-p[0])**2 + (y-p[1])**2))
        lit = ((x - a) + (y - b)) / r / 1.414
        put(x, y, W if lit < -0.1 else L if lit < 0.45 else G)
        if len(hits) >= 2 and all((x-a)**2 + (y-b)**2 > (r-1.0)**2 for a, b, r in hits):
            put(x, y, G)                   # crease between two lobes
for x, y in [(x, y) for y in range(N) for x in range(N) if not inside(x, y)
             and any(inside(x+dx, y+dy) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)])]:
    if px[x, y][3] == 0:
        put(x, y, OUT)

img.resize((N*4, N*4), Image.NEAREST).save(sys.argv[1])
