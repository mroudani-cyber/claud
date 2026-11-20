import random, math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = os.path.join(os.path.dirname(__file__), 'out'); os.makedirs(OUT, exist_ok=True)
S = 128
def hexc(h, a=255): h = h.lstrip('#'); return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), a)
def shade(c, f): return tuple(max(0, min(255, int(v*f))) for v in c[:3]) + (c[3],)

# ---------------------------------------------------------------- sprites (16x16 ascii, palette)
def sprite(rows, pal):
    n = max(len(r) for r in rows); im = Image.new('RGBA', (16, 16), (0,0,0,0))
    oy = (16 - len(rows)) // 2; ox = (16 - n) // 2
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != '.': im.putpixel((x+ox, y+oy), pal[ch] if isinstance(pal[ch], tuple) else hexc(pal[ch]))
    return im
def up(im16, pad=0):
    big = im16.resize((S - 2*pad, S - 2*pad), Image.NEAREST)
    out = Image.new('RGBA', (S, S), (0,0,0,0)); out.paste(big, (pad, pad), big); return out
def drop(im, off=4, a=70):
    sh = Image.new('RGBA', im.size, (0,0,0,0)); m = im.split()[3].point(lambda v: a if v else 0)
    sh.putalpha(m); sh = sh.filter(ImageFilter.GaussianBlur(2))
    out = Image.new('RGBA', im.size, (0,0,0,0)); out.paste(sh, (off//2, off), sh); out.paste(im, (0,0), im); return out
def save(im, name): drop(im).save(f'{OUT}/{name}.png')

SWORD = [
".............ooo",
"............ohho",
"...........ohhmo",
"..........ohhmo.",
".........ohhmo..",
"........ohhmo...",
".......ohhmo....",
"..oo..ohhmo.....",
"..ogoohhmo......",
"...ogghmo.......",
"....oggo........",
"...owoggo.......",
"..owo.ogGo......",
".owo...oo.......",
"oeo.............",
"oo..............",
]
TIERS = {
 'wood':      dict(h='#c49a5c', m='#9a7440', d='#6b4f29'),
 'stone':     dict(h='#b0b0b0', m='#8a8a8a', d='#5e5e5e'),
 'iron':      dict(h='#ffffff', m='#d8d8d8', d='#9c9c9c'),
 'gold':      dict(h='#fff6a8', m='#fad64a', d='#c99a1a'),
 'diamond':   dict(h='#d6fffa', m='#4aedd9', d='#1f9e8e'),
 'netherite': dict(h='#6d6470', m='#4a434d', d='#2b262e'),
}
def tool_pal(t): c = TIERS[t]; return {'o':'#1b1b1b','h':c['h'],'m':c['m'],'d':c['d'],'g':'#3d2a14','G':'#5c3f1f','w':'#7a5530','e':'#4a3218'}
for t in ['wood','stone','iron','gold','diamond','netherite']:
    save(up(sprite(SWORD, tool_pal(t)), 8), f'mc_sword_{t}')

PICK = [
"...ooooooooo....",
"..ohhhhhmmmmo...",
".ohhmmmmmmmddo..",
".ohmmooooowdddo.",
".omo....owo.odo.",
".oo....owo...odo",
".......owo....oo",
"......owo.......",
".....owo........",
"....owo.........",
"...owo..........",
"..owo...........",
".owo............",
"oeo.............",
"oo..............",
]
AXE = [
".......ooooo....",
"......ohhhmmo...",
".....ohhmmmmdo..",
".....ohmmmmwddo.",
"......ommmowddo.",
".......oooowdo..",
"........owoo....",
"........owo.....",
".......owo......",
"......owo.......",
".....owo........",
"....owo.........",
"...owo..........",
"..owo...........",
".oeo............",
".oo.............",
]
for t in ['iron','gold','diamond','netherite']: save(up(sprite(PICK, tool_pal(t)), 8), f'mc_pickaxe_{t}')
for t in ['diamond','netherite']: save(up(sprite(AXE, tool_pal(t)), 8), f'mc_axe_{t}')

HELM = [
"....oooooooo....",
"..oohhhhhmmmoo..",
".ohhhmmmmmmmmdo.",
".ohhmmmmmmmmmdo.",
".ohmmmmmmmmmmdo.",
".ohmmmmmmmmmmdo.",
".ohmmoooooommdo.",
".ohmo......omdo.",
".ohmo......omdo.",
".oddo......oddo.",
"..oo........oo..",
]
CHEST = [
".ooooo....ooooo.",
"ohhmmdo..ohmmddo",
"ohmmmdoooohmmmdo",
"ohmmmmhhhmmmmmdo",
".ommmmhmmmmmmdo.",
"..ohmmmmmmmmdo..",
"..ohmmmmmmmmdo..",
"..ohmmmmmmmmdo..",
"..ohmmmmmmmmdo..",
"..ohmmmmmmmmdo..",
"..odddddddddd o.".replace(' ','d'),
"..oooooooooooo..",
]
for t in ['iron','gold','diamond','netherite']:
    p = tool_pal(t); save(up(sprite(HELM, p), 8), f'mc_helmet_{t}'); save(up(sprite(CHEST, p), 8), f'mc_chestplate_{t}')

GEM = [
"......oooo......",
".....ohhhmo.....",
"....ohhmmmdo....",
"...ohhmmmmmdo...",
"..ohhmmmmmmmdo..",
"..odmmmmmmmmdo..",
"...odmmmmmmdo...",
"....odmmmmdo....",
".....oddddo.....",
"......oooo......",
]
INGOT = [
"......oooooooo..",
".....ohhhhhhmo..",
"....ohhmmmmmdo..",
"...ohhmmmmmdo...",
"..ohhmmmmmmdo...",
".ooooooooodo....",
".ohhhhhhhmdo....",
".ommmmmmmmo.....",
".oddddddddo.....",
".oooooooooo.....",
]
save(up(sprite(GEM, {'o':'#0c3b36','h':'#e8fffc','m':'#4aedd9','d':'#1a8a7c'}), 10), 'mc_diamond')
save(up(sprite(GEM, {'o':'#0b3d1c','h':'#d6ffd9','m':'#41d86a','d':'#17863a'}), 10), 'mc_emerald')
save(up(sprite(INGOT, {'o':'#5a3d00','h':'#fff6a8','m':'#fad64a','d':'#c99a1a'}), 10), 'mc_gold_ingot')
save(up(sprite(INGOT, {'o':'#333333','h':'#ffffff','m':'#d8d8d8','d':'#9c9c9c'}), 10), 'mc_iron_ingot')
save(up(sprite(INGOT, {'o':'#121012','h':'#857b88','m':'#4a434d','d':'#2b262e'}), 10), 'mc_netherite_ingot')

APPLE = [
".......oo.......",
"......ogo.oo....",
".....oooggo.....",
"...ooyyoooyoo...",
"..oyhhyyyyyydo..",
".oyhhyyyyyyyydo.",
".oyhyyyyyyyyydo.",
".oyyyyyyyyyyydo.",
".oyyyyyyyyyyydo.",
"..oyyyyyyyyydo..",
"..odyyyyyyyddo..",
"...oddyyyyddo...",
"....oooddooo....",
".......oo.......",
]
save(up(sprite(APPLE, {'o':'#3a2a00','g':'#5b8f2a','y':'#fad64a','h':'#fffbd0','d':'#c99a1a'}), 8), 'mc_golden_apple')
PEARL = [
".....oooooo.....",
"...oohhmmmmoo...",
"..ohhmmmmmmmdo..",
".ohhmmccmmmmmdo.",
".ohmmcffcmmmmdo.",
".ommmcffcmmmmdo.",
".ommmmccmmmmmdo.",
".ommmmmmmmmmddo.",
"..odmmmmmmmddo..",
"...ooddddddoo...",
".....oooooo.....",
]
save(up(sprite(PEARL, {'o':'#06231e','h':'#7ff0c8','m':'#1f7a66','d':'#0f4a3d','c':'#2eb894','f':'#0a2e26'}), 10), 'mc_ender_pearl')
POT = [
".....oooooo.....",
".....owwwwo.....",
"......oggo......",
"......oggo......",
".....ogllgo.....",
"....ollllllo....",
"...ollhlllllo...",
"..olhhllllllllo.".replace('llllllllo','lllllldo'),
"..olhlllllllldo.",
"..ollllllllldo..".replace('do..','ddo.'),
"..ollllllllldo..",
"...oddllllddo...",
"....oooooooo....",
]
def potion(name, liq, hi, dk):
    save(up(sprite(POT, {'o':'#1b1b1b','w':'#8a6a3a','g':'#d9e8ef','l':liq,'h':hi,'d':dk}), 8), name)
potion('mc_potion_heal', '#e8384f', '#ffb3bd', '#8f1626')
potion('mc_potion_speed', '#7cc4ff', '#e0f2ff', '#2f6fae')
potion('mc_potion_fire', '#ff9a2e', '#ffe0b0', '#b35a00')
potion('mc_potion_strength', '#b0233a', '#ff8a9a', '#5e0f1c')
potion('mc_potion_poison', '#5aa832', '#c8f0a8', '#2c5e14')
TOTEM = [
"....oooooooo....",
"...ohhhhhhmmo...",
"...ohkhhhhkmo...",
"...ohhhhhhhmo...",
"...ohhggggmmo...",
"....oooggooo....",
"..oggggggggggo..",
".ogoohhhhhhoogo.",
".oo.ohhhhhhmo.oo",
"....ohhggmmmo...",
"....ohggggmmo...",
"....ooggggmoo...",
".....ooooooo....",
]
save(up(sprite(TOTEM, {'o':'#3a2a00','h':'#fbe27a','m':'#d9a823','k':'#1b5e20','g':'#41a85a'}), 8), 'mc_totem')
STAR = [
".......oo.......",
"......ohho......",
"......ohmo......",
".....ohhmmo.....",
"ooooohhhmmmooooo",
"ohhhhhhhmmmmmmdo",
".oohhhhmmmmmdoo.",
"...ohhhmmmmdo...",
"...ohhmmmmmdo...",
"..ohhmmooommdo..",
"..ohmoo...oomdo.",
".ohoo.......oodo",
".oo...........oo",
]
save(up(sprite(STAR, {'o':'#4b4b6e','h':'#ffffff','m':'#e7e7ff','d':'#b5b5d6'}), 8), 'mc_nether_star')
BOW = [
"..........oooo..",
"........oowwwo..",
"......oowwoos...",
".....owwoo.s....",
"....owoo...s....",
"...owo....s.....",
"...owo....s.....",
"..owo....s......",
"..owo....s......",
"..owo...s.......",
"...owo..s.......",
"...owwoos.......",
"....oooo........",
]
save(up(sprite(BOW, {'o':'#2a1a08','w':'#8f6a3a','s':'#e6e6e6'}), 8), 'mc_bow')
SHIELD = [
"..oooooooooooo..",
".ohhhhhhmmmmmdo.",
".ohwwwwwwwwwwdo.",
".ohwrrrrrrrrwdo.",
".ohwrryyyyrrwdo.",
".ohwrryyyyrrwdo.",
".ohwrrrrrrrrwdo.",
"..ohwrrrrrrwdo..",
"..ohwrrrrrrwdo..",
"...ohwrrrrwdo...",
"....ohwwwwdo....",
".....ohhddo.....",
"......oooo......",
]
save(up(sprite(SHIELD, {'o':'#1b1b1b','h':'#d8d8d8','m':'#9c9c9c','d':'#6e6e6e','w':'#8f6a3a','r':'#7a2bd6','y':'#f5c542'}), 8), 'mc_shield')

ARROW = [
"...........oooo.",
"..........ohhho.",
"..........ohmmo.",
".........owomo..",
"........owo.o...",
".......owo......",
"......owo.......",
".....owo........",
"..o.owo.........",
".owowo..........",
".offo...........",
"offo............",
".oo.............",
]
save(up(sprite(ARROW, {'o':'#1b1b1b','h':'#e6e6e6','m':'#9c9c9c','w':'#8f6a3a','f':'#f2f2f2'}), 8), 'mc_arrow')
ROD = [
"...........oo...",
"..........owwo..",
".........owwos..",
"........owwo.s..",
".......owwo..s..",
"......owwo...s..",
".....owwo....s..",
"....owwo.....s..",
"...owwo......s..",
"..owwo......ooo.",
".oxwo.......ohso",
".oxo.........oo.",
"..o.............",
]
save(up(sprite(ROD, {'o':'#1b1b1b','w':'#8f6a3a','x':'#5c3f1f','s':'#d8d8d8','h':'#c0c0c0'}), 8), 'mc_fishing_rod')
COMP = [
".....oooooo.....",
"...ooggggggoo...",
"..oggwwwwwwggo..",
".ogwwwwrwwwwwgo.",
".ogwwwwrrwwwwgo.",
".ogwwwwrrwwwwgo.",
".ogwwwwkbwwwwgo.",
".ogwwwwbbwwwwgo.",
".ogwwwwbwwwwwgo.",
"..oggwwwwwwggo..",
"...ooggggggoo...",
".....oooooo.....",
]
save(up(sprite(COMP, {'o':'#1b1b1b','g':'#9c9c9c','w':'#e8e8e8','r':'#d93a2b','b':'#5e5e5e','k':'#1b1b1b'}), 8), 'mc_compass')

# ---------------------------------------------------------------- isometric blocks
def tex(base, var=0.12, spots=None, seed=1, pattern=None):
    r = random.Random(seed); t = Image.new('RGBA', (16,16))
    for y in range(16):
        for x in range(16):
            f = 1 + r.uniform(-var, var); c = shade(hexc(base), f)
            if pattern: c = pattern(x, y, c, r) or c
            t.putpixel((x,y), c)
    if spots:
        for col, n, size in spots:
            for _ in range(n):
                sx, sy = r.randrange(1, 14), r.randrange(1, 14)
                for dx in range(size):
                    for dy in range(size):
                        if r.random() < .8: t.putpixel(((sx+dx)%16, (sy+dy)%16), shade(hexc(col), r.uniform(.85,1.15)))
    return t
def iso(top, left, right):
    # 128x128 isometric cube via inverse mapping
    im = Image.new('RGBA', (S,S), (0,0,0,0)); px = im.load()
    cx, w, h = 64, 54, 27   # half width, half height of top rhombus
    ty = 14                 # top vertex
    side = 62
    T, L, R = top.load(), left.load(), right.load()
    for Y in range(S):
        for X in range(S):
            dx, dy = X + .5 - cx, Y + .5 - (ty + h)
            # top face: u along +x-down, v along -x-down
            u = (dx / w + dy / h) / 2 + .5; v = (-dx / w + dy / h) / 2 + .5
            if 0 <= u < 1 and 0 <= v < 1:
                px[X, Y] = T[int(u*16), int(v*16)]; continue
            if X < cx:   # left face
                a = (X - (cx - w)) / w
                yb = ty + h + a * h
                b = (Y - yb) / side
                if 0 <= a < 1 and 0 <= b < 1:
                    c = L[int(a*16), int(b*16)]; px[X, Y] = shade(c, .78)
            else:
                a = (X - cx) / w
                yb = ty + 2*h - a * h
                b = (Y - yb) / side
                if 0 <= a < 1 and 0 <= b < 1:
                    c = R[int(a*16), int(b*16)]; px[X, Y] = shade(c, .6)
    # outline
    d = ImageDraw.Draw(im)
    pts = [(cx, ty), (cx+w, ty+h), (cx+w, ty+h+side), (cx, ty+2*h+side), (cx-w, ty+h+side), (cx-w, ty+h)]
    d.line(pts + [pts[0]], fill=(20,20,20,255), width=3, joint='curve')
    d.line([(cx-w, ty+h), (cx, ty+2*h), (cx+w, ty+h)], fill=(255,255,255,70), width=2)
    d.line([(cx, ty+2*h), (cx, ty+2*h+side)], fill=(0,0,0,90), width=2)
    return im
def block(name, top, side=None, front=None):
    side = side or top; save(iso(top, side, front or side), name)
stone = tex('#7d7d7d', .14, seed=3)
dirt = tex('#866043', .16, spots=[('#6b4a30', 10, 2), ('#9c7552', 8, 1)], seed=4)
grass_top = tex('#5fa83a', .16, spots=[('#4a8c2a', 12, 1), ('#79c24e', 10, 1)], seed=5)
grass_side = dirt.copy()
for x in range(16):
    for y in range(4 + (x*7 % 3)): grass_side.putpixel((x, y), shade(hexc('#5fa83a'), random.Random(x*9+y).uniform(.85, 1.1)))
block('mc_grass', grass_top, grass_side)
block('mc_dirt', dirt)
block('mc_stone', stone)
cob = tex('#7a7a7a', .1, seed=6, pattern=lambda x,y,c,r: shade(c,.62) if (x+3*(y//4))%5==0 or y%4==0 else (shade(c,1.18) if (x+y)%7==1 else None))
block('mc_cobblestone', cob)
for nm, col in [('diamond', '#4aedd9'), ('gold', '#fad64a'), ('iron', '#d8af93'), ('emerald', '#41d86a'), ('redstone', '#e01b1b'), ('coal', '#1d1d1d'), ('lapis', '#2457c9')]:
    t = tex('#7d7d7d', .12, spots=[(col, 6, 2)], seed=hash(nm) % 99)
    block(f'mc_{nm}_ore', t)
block('mc_obsidian', tex('#140f20', .25, spots=[('#3b2a5e', 9, 2)], seed=8))
block('mc_netherrack', tex('#6f2a2a', .2, spots=[('#8f3b3b', 10, 2), ('#4a1a1a', 8, 1)], seed=9))
block('mc_end_stone', tex('#dbe0a2', .08, spots=[('#c6cb8d', 10, 2)], seed=10))
block('mc_sand', tex('#dbcf97', .08, seed=11))
planks = tex('#a2824e', .07, seed=12, pattern=lambda x,y,c,r: shade(c,.68) if y%4==3 else (shade(c,.82) if (x+ (y//4)*5)%8==0 else None))
block('mc_planks', planks)
logtop = tex('#a2824e', .05, seed=13, pattern=lambda x,y,c,r: shade(hexc('#6b5232'),1) if max(abs(x-7.5),abs(y-7.5))>6.5 else (shade(c,.8) if int(max(abs(x-7.5),abs(y-7.5)))%2==0 else None))
logside = tex('#6b5232', .12, seed=14, pattern=lambda x,y,c,r: shade(c,.7) if x%3==0 else None)
block('mc_log', logtop, logside)
tnt_side = tex('#d93a2b', .06, seed=15, pattern=lambda x,y,c,r: (hexc('#e8e8e8') if 6<=y<=9 else (shade(c,.75) if x%4==0 else None)))
for i, ch in enumerate([[0,1,1,1,0],[0,1,1,0,1],[0,1,1,1,0]]): pass
d = ImageDraw.Draw(tnt_side); d.text((2, 5), 'TNT', fill=(30,30,30,255), font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 5))
tnt_top = tex('#d93a2b', .06, seed=16, pattern=lambda x,y,c,r: hexc('#e8e8e8') if 6<=x<=9 and 6<=y<=9 else None)
block('mc_tnt', tnt_top, tnt_side)
glow = tex('#e8b04a', .25, spots=[('#fff2a8', 12, 2), ('#a36b1f', 8, 1)], seed=17)
block('mc_glowstone', glow)
ct_top = tex('#a2824e', .07, seed=18, pattern=lambda x,y,c,r: shade(c,.55) if x in (0,15) or y in (0,15) or x==7 or y==7 else None)
ct_side = planks.copy(); d = ImageDraw.Draw(ct_side); d.rectangle([3,3,6,8], fill=hexc('#8a8a8a')); d.rectangle([9,3,12,8], fill=hexc('#6b4a30'))
block('mc_crafting_table', ct_top, ct_side)
bs = planks.copy(); r = random.Random(19)
for row in (1, 9):
    x = 1
    while x < 15:
        col = r.choice(['#8f2a2a', '#2a5e8f', '#2a8f4a', '#8f7a2a', '#5e2a8f']); w = r.choice([1,2])
        for xx in range(x, min(15, x+w)):
            for yy in range(row, row+5): bs.putpixel((xx, yy), shade(hexc(col), r.uniform(.85, 1.1)))
        x += w + 0
block('mc_bookshelf', planks, bs)

# ---------------------------------------------------------------- PvP tier badges
F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
TIERC = {1: ('#ffd54a', '#b8860b'), 2: ('#e0e6ee', '#8c97a6'), 3: ('#e8975a', '#9c5427'), 4: ('#7fd1ff', '#2f86c2'), 5: ('#b9a6ff', '#6c55c7')}
def badge(text, top, bot, name, high=True):
    im = Image.new('RGBA', (S,S), (0,0,0,0))
    g = Image.new('RGBA', (S,S)); gd = ImageDraw.Draw(g)
    a, b = hexc(top), hexc(bot)
    for y in range(S):
        t = y / S; gd.line([(0,y),(S,y)], fill=tuple(int(a[i]*(1-t)+b[i]*t) for i in range(3)) + (255,))
    m = Image.new('L', (S,S), 0); md = ImageDraw.Draw(m)
    shape = [(64,6),(118,24),(112,82),(64,122),(16,82),(10,24)]
    md.polygon(shape, fill=255)
    im.paste(g, (0,0), m)
    d = ImageDraw.Draw(im)
    d.polygon(shape, outline=(25,25,30,255), width=6)
    inner = [(64,16),(108,31),(103,78),(64,111),(25,78),(20,31)]
    d.line(inner + [inner[0]], fill=(255,255,255,110 if high else 60), width=3)
    f = ImageFont.truetype(F, 33)
    w = d.textlength(text, font=f)
    d.text(((S-w)/2, 42), text, font=f, fill=(255,255,255,255), stroke_width=4, stroke_fill=(25,25,30,255))
    if high:
        d.polygon([(64,92),(70,100),(64,108),(58,100)], fill=(255,255,255,230))
    return im
for n in range(1, 6):
    top, bot = TIERC[n]
    save(badge(f'HT{n}', top, bot, f'tier_ht{n}'), f'tier_ht{n}')
    save(badge(f'LT{n}', shade(hexc(top), .85)[:3] and '#%02x%02x%02x' % shade(hexc(top), .82)[:3], bot, f'tier_lt{n}', high=False), f'tier_lt{n}')
print(len(os.listdir(OUT)), 'static')
