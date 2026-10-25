"""Draws extras/polydex-bar: the bar themes for "/polydex color" on our server.

The server (mc/mods-src/polydex-bar in homelab-iac) gives each theme a boss
bar colour and overlay nothing else uses; this pack draws those sprites.
Yellow is see-through: the bar while it only names a block, and the base
under the notched themes, so those can be thinner than vanilla's 5 pixels.

    python3 .github/make-bar.py [preview.png]   (the pack; a preview too if named)
"""
import json, pathlib, random, struct, sys, zlib

W, H = 182, 5
OUT = pathlib.Path(__file__).resolve().parent.parent / "extras/polydex-bar"
SPRITES = OUT / "assets/minecraft/textures/gui/sprites/boss_bar"

# name: (sprite slot, track RGBA, fill top, fill middle, fill bottom, speck or None)
THEMES = {
    "obsidian": ("notched_6", (18, 10, 28, 210), (112, 72, 170), (66, 36, 110), (36, 18, 60), (160, 120, 220)),
    "dark":     ("notched_12", (28, 28, 32, 220), (232, 232, 236), (196, 196, 202), (140, 140, 148), None),
    "cotton":   ("notched_20", (92, 72, 52, 170), (255, 255, 250), (244, 237, 224), (212, 198, 178), None),
    "emerald":  ("green", (10, 40, 24, 200), (120, 240, 160), (40, 190, 100), (20, 128, 64), (190, 255, 210)),
    "copper":   ("blue", (46, 26, 14, 200), (242, 172, 122), (200, 116, 60), (148, 80, 40), (255, 210, 170)),
}


def png(px, w, h):
    raw = b"".join(b"\0" + b"".join(bytes(px[y][x]) for x in range(w)) for y in range(h))
    ch = lambda k, v: struct.pack(">I", len(v)) + k + v + struct.pack(">I", zlib.crc32(k + v))
    return (b"\x89PNG\r\n\x1a\n" + ch(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + ch(b"IDAT", zlib.compress(raw, 9)) + ch(b"IEND", b""))


def blank():
    return [[(0, 0, 0, 0)] * W for _ in range(H)]


def inside(x, y):
    """A 3-pixel bar (rows 1-3) with rounded ends: a little smaller than vanilla."""
    if not (1 <= y <= 3 and 1 <= x <= W - 2):
        return False
    return y == 2 or 2 <= x <= W - 3


def theme(track, top, mid, bottom, speck, seed):
    bg, fg = blank(), blank()
    rnd = random.Random(seed)
    specks = {x for x in range(4, W - 4) if rnd.random() < 0.07} if speck else set()
    for y in range(H):
        for x in range(W):
            if inside(x, y):
                bg[y][x] = track
                c = (top, mid, bottom)[y - 1]
                fg[y][x] = (*(speck if y == 2 and x in specks else c), 255)
    return bg, fg


def write(name, px):
    (SPRITES / f"{name}.png").write_bytes(png(px, W, H))


SPRITES.mkdir(parents=True, exist_ok=True)
write("yellow_background", blank())
write("yellow_progress", blank())
bars = {}
for i, (name, (slot, *t)) in enumerate(THEMES.items()):
    bars[name] = theme(*t, seed=i)
    write(f"{slot}_background", bars[name][0])
    write(f"{slot}_progress", bars[name][1])
(OUT / "pack.mcmeta").write_text(json.dumps({"pack": {
    "description": "CottonCraft: Polydex bar themes (/polydex color) and names only",
    "min_format": 97, "max_format": 999}}, indent=1) + "\n")

# Preview, not in the pack: each theme at 60 %, over sky and over stone, 4x.
if len(sys.argv) < 2:
    sys.exit()
S, rows = 4, []
for sky in ((120, 167, 255), (110, 110, 110)):
    for bg, fg in bars.values():
        line = []
        for x in range(W):
            col = []
            for y in range(H):
                p = fg[y][x] if x < W * 0.6 and fg[y][x][3] else bg[y][x]
                a = p[3] / 255
                col.append(tuple(round(p[i] * a + sky[i] * (1 - a)) for i in range(3)) + (255,))
            line.append(col)
        for y in range(H + 3):
            rows.append([line[x][y] if y < H else (*sky, 255) for x in range(W)])
big = [[r[x // S] for x in range(W * S)] for r in rows for _ in range(S)]
pathlib.Path(sys.argv[1]).write_bytes(png(big, W * S, len(big)))
