import os, math
from PIL import Image, ImageDraw, ImageFont, ImageChops
D = os.path.dirname(os.path.abspath(__file__)); IN = f'{D}/out'; OUT = f'{D}/anim'; os.makedirs(OUT, exist_ok=True)
S = 128; F = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def load(n): return Image.open(f'{IN}/{n}.png').convert('RGBA')
def solid(im):  # drop the soft shadow (GIF has 1-bit alpha)
    a = im.split()[3].point(lambda v: 255 if v >= 200 else 0); im = im.copy(); im.putalpha(a); return im
def save_gif(frames, name, ms=70):
    pal = []
    for f in frames:
        a = f.split()[3]
        p = f.convert('RGB').quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        p.paste(255, mask=a.point(lambda v: 255 if v < 128 else 0))
        p.info['transparency'] = 255; pal.append(p)
    pal[0].save(f'{OUT}/{name}.gif', save_all=True, append_images=pal[1:], duration=ms, loop=0, disposal=2, transparency=255, optimize=False)
def glint(base, n=16, col=(190, 110, 255)):
    base = solid(base); a = base.split()[3]; frames = []
    for i in range(n):
        band = Image.new('L', (S, S), 0); d = ImageDraw.Draw(band)
        off = -S + i * (3 * S // n)
        for k, w, v in [(0, 26, 150), (40, 10, 90)]:
            d.polygon([(off + k, 0), (off + k + w, 0), (off + k + w - S, S), (off + k - S, S)], fill=v)
        band = ImageChops.multiply(band, a)
        over = Image.new('RGBA', (S, S), col + (0,)); over.putalpha(band)
        fr = base.copy(); fr.alpha_composite(over); frames.append(fr)
    return frames
def shine(base, n=18): return glint(base, n, (255, 255, 255))
def bob(base, n=16, amp=7):
    base = solid(base); frames = []
    for i in range(n):
        y = round(math.sin(i / n * 2 * math.pi) * amp)
        fr = Image.new('RGBA', (S, S), (0,0,0,0)); fr.alpha_composite(base, (0, y)); frames.append(fr)
    return frames
# 1) enchanted gear (purple glint) x12
for n in ['mc_sword_diamond', 'mc_sword_netherite', 'mc_sword_gold', 'mc_sword_iron', 'mc_golden_apple', 'mc_pickaxe_diamond',
          'mc_chestplate_diamond', 'mc_chestplate_netherite', 'mc_helmet_diamond', 'mc_bow', 'mc_shield', 'mc_nether_star']:
    save_gif(glint(load(n)), 'ench_' + n[3:])
# 2) tier badges shine x5
for t in range(1, 6): save_gif(shine(load(f'tier_ht{t}')), f'tier_ht{t}_shine')
# 3) floating items x4
for n in ['mc_diamond', 'mc_emerald', 'mc_totem', 'mc_ender_pearl']: save_gif(bob(load(n)), 'float_' + n[3:])
# 4) TNT flashing
tnt = solid(load('mc_tnt')); fr = []
for i in range(10):
    f = tnt.copy()
    if i % 2:
        w = Image.new('RGBA', (S, S), (255, 255, 255, 0)); w.putalpha(tnt.split()[3].point(lambda v: 170 if v else 0)); f.alpha_composite(w)
    fr.append(f)
save_gif(fr, 'anim_tnt', 180)
# 5) status icons x8
def frames_draw(fn, n): return [fn(i, n) for i in range(n)]
def canvas(): return Image.new('RGBA', (S, S), (0,0,0,0))
def dot(i, n, col):
    im = canvas(); d = ImageDraw.Draw(im); p = (math.sin(i / n * 2 * math.pi) + 1) / 2
    r = 26 + p * 22; d.ellipse([64-r, 64-r, 64+r, 64+r], fill=col + (int(110 - p * 80),))
    d.ellipse([34, 34, 94, 94], fill=col + (255,), outline=(20,20,20,255), width=6)
    d.ellipse([46, 42, 62, 56], fill=(255,255,255,170)); return im
save_gif(frames_draw(lambda i, n: dot(i, n, (59, 201, 99)), 14), 'status_online', 80)
save_gif(frames_draw(lambda i, n: dot(i, n, (240, 178, 50)), 14), 'status_idle', 80)
def pill(text, col, i, n, flash=True):
    im = canvas(); d = ImageDraw.Draw(im); on = (i // (n // 2)) == 0 or not flash
    c = col if on else tuple(int(v * .7) for v in col)
    d.rounded_rectangle([6, 34, 122, 94], 18, fill=c + (255,), outline=(20,20,20,255), width=6)
    f = ImageFont.truetype(F, 36); w = d.textlength(text, font=f)
    d.text(((S - w) / 2, 42), text, font=f, fill=(255,255,255,255), stroke_width=3, stroke_fill=(20,20,20,255))
    if on and text == 'LIVE': d.ellipse([12, 56, 22, 66], fill=(255,255,255,255))
    return im
save_gif(frames_draw(lambda i, n: pill('LIVE', (230, 45, 60), i, n), 10), 'badge_live', 120)
save_gif(frames_draw(lambda i, n: pill('NEW', (122, 76, 236), i, n), 10), 'badge_new', 120)
save_gif(shine(pill('HOT', (245, 120, 30), 0, 2, False)), 'badge_hot')
def spinner(i, n):
    im = canvas(); d = ImageDraw.Draw(im)
    for k in range(8):
        a = (k / 8) * 2 * math.pi; x, y = 64 + math.cos(a) * 40, 64 + math.sin(a) * 40
        v = ((k - i) % 8) / 8; r = 7 + (1 - v) * 7
        d.ellipse([x - r, y - r, x + r, y + r], fill=(139, 92, 246, int(255 - v * 200)), outline=(20,20,20,int(255 - v*200)), width=3)
    return im
save_gif(frames_draw(spinner, 8), 'status_loading', 90)
def check(i, n):
    im = canvas(); d = ImageDraw.Draw(im); s = min(1, (i + 1) / 5) if i < 5 else 1 + 0.06 * math.sin(i)
    r = 50 * s; d.ellipse([64-r, 64-r, 64+r, 64+r], fill=(46, 184, 92, 255), outline=(20,20,20,255), width=6)
    if i >= 3: d.line([(40, 66), (57, 82), (90, 46)], fill=(255,255,255,255), width=13, joint='curve')
    return im
save_gif(frames_draw(check, 12), 'anim_check', 80)
def warn(i, n):
    im = canvas(); d = ImageDraw.Draw(im); c = (245, 190, 40) if i % 2 == 0 else (255, 120, 40)
    d.polygon([(64, 10), (122, 112), (6, 112)], fill=c + (255,), outline=(20,20,20,255), width=6)
    d.rounded_rectangle([57, 42, 71, 82], 5, fill=(30,30,30,255)); d.ellipse([56, 88, 72, 104], fill=(30,30,30,255)); return im
save_gif(frames_draw(warn, 6), 'anim_alert', 220)
def heart(i, n):
    im = canvas(); d = ImageDraw.Draw(im); s = 1 + 0.12 * max(0, math.sin(i / n * 2 * math.pi)) ** 3
    P = [(64, 112), (14, 58), (14, 34), (34, 16), (52, 18), (64, 32), (76, 18), (94, 16), (114, 34), (114, 58)]
    P = [(64 + (x - 64) * s, 64 + (y - 64) * s) for x, y in P]
    d.polygon(P, fill=(232, 56, 79, 255), outline=(20,20,20,255), width=6)
    d.ellipse([30 * s + 64 * (1 - s), 30 * s + 64 * (1 - s), 46 * s + 64 * (1 - s), 44 * s + 64 * (1 - s)], fill=(255, 200, 210, 255)); return im
save_gif(frames_draw(heart, 14), 'anim_heart', 70)
print(len(os.listdir(OUT)), 'animated', [ (f, os.path.getsize(f'{OUT}/{f}')//1024) for f in sorted(os.listdir(OUT)) if os.path.getsize(f'{OUT}/{f}') > 200_000])
