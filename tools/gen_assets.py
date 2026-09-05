import numpy as np, math, os
from PIL import Image, ImageFilter, ImageDraw

rng = np.random.default_rng(7)

def smoothstep(t): return t*t*(3-2*t)

def value_noise(h, w, res, seed=0):
    r = np.random.default_rng(seed)
    gh, gw = res, max(1, int(res*w/h))
    grid = r.random((gh+1, gw+1))
    ys = np.linspace(0, gh, h, endpoint=False)
    xs = np.linspace(0, gw, w, endpoint=False)
    y0 = np.floor(ys).astype(int); x0 = np.floor(xs).astype(int)
    fy = smoothstep(ys-y0)[:,None]; fx = smoothstep(xs-x0)[None,:]
    g00 = grid[np.ix_(y0, x0)]; g10 = grid[np.ix_(y0+1, x0)]
    g01 = grid[np.ix_(y0, x0+1)]; g11 = grid[np.ix_(y0+1, x0+1)]
    return (g00*(1-fy)*(1-fx) + g10*fy*(1-fx) + g01*(1-fy)*fx + g11*fy*fx)

def fbm(h, w, octaves=6, res=3, seed=0, gain=0.5):
    out = np.zeros((h,w)); amp = 1.0; tot = 0.0
    for o in range(octaves):
        out += amp*value_noise(h, w, res*(2**o), seed=seed+o*13)
        tot += amp; amp *= gain
    return out/tot

def norm(a):
    a = a - a.min()
    return a/(a.max()+1e-9)

def ramp(x, stops):
    """stops: list of (pos, (r,g,b))"""
    x = np.clip(x,0,1)
    out = np.zeros(x.shape+(3,))
    ps = [s[0] for s in stops]
    for i in range(len(stops)-1):
        p0,c0 = stops[i]; p1,c1 = stops[i+1]
        m = (x>=p0)&(x<=p1)
        t = np.zeros_like(x); t[m] = (x[m]-p0)/max(1e-9,(p1-p0))
        for c in range(3):
            out[...,c] += m*(c0[c]+(c1[c]-c0[c])*t)/255.0
    out[x<=ps[0]] = np.array(stops[0][1])/255.0
    out[x>=ps[-1]] = np.array(stops[-1][1])/255.0
    return out

def save(arr, path, q=88):
    img = Image.fromarray(np.clip(arr,0,255).astype(np.uint8))
    if path.endswith('.jpg'): img.save(path, quality=q, optimize=True, progressive=True)
    else: img.save(path, optimize=True)
    print('  ->', path, img.size, f"{os.path.getsize(path)/1024:.0f}KB")

def grain_layer(h,w,amount=8, seed=1):
    r = np.random.default_rng(seed)
    return (r.normal(0,1,(h,w,1))*amount)

H, W = 1400, 2200

# ---------------------------------------------------------------- 1. ARC FIELD
def arc_field(path, hue='ember'):
    h,w = H,W
    yy,xx = np.mgrid[0:h,0:w].astype(float)
    cx, cy = w*0.62, h*0.44
    d = np.sqrt(((xx-cx)/w)**2 + ((yy-cy)/h*1.6)**2)
    core = np.exp(-d*7.0)
    halo = np.exp(-d*2.2)*0.55
    # anisotropic streaks radiating from core
    ang = np.arctan2(yy-cy, xx-cx)
    streak = norm(fbm(h,w,5,4,seed=21))
    rays = (0.5+0.5*np.sin(ang*46 + streak*9))**3
    rays = rays*np.exp(-d*3.4)*0.5
    turb = norm(fbm(h,w,7,3,seed=44))
    smoke = turb*np.exp(-d*1.1)*0.35
    v = norm(core*1.5 + halo + rays + smoke*0.8)
    if hue=='ember':
        stops=[(0.0,(6,6,9)),(0.22,(24,17,20)),(0.44,(96,26,22)),(0.62,(196,52,26)),(0.8,(240,120,44)),(1.0,(255,231,196))]
    else:
        stops=[(0.0,(5,6,10)),(0.24,(12,20,42)),(0.48,(20,52,120)),(0.68,(46,110,214)),(0.86,(140,190,255)),(1.0,(240,248,255))]
    img = ramp(v, stops)*255
    # scanline / sensor texture
    img *= (1 + 0.03*np.sin(yy*math.pi*0.9))[...,None]
    img += grain_layer(h,w,6.5,seed=3)
    # vignette
    vg = 1-0.55*norm(((xx/w-0.5)**2*1.1+(yy/h-0.5)**2))
    img *= vg[...,None]
    save(img, path)

# ------------------------------------------------------- 2. STEEL LATTICE PLATE
def lattice(path, tone='steel'):
    h,w = H,W
    im = Image.new('L',(w,h),0); dr = ImageDraw.Draw(im)
    r = np.random.default_rng(11)
    # perspective truss: several depth planes
    for depth in range(5):
        z = 0.4+depth*0.42
        alpha = int(240/ (1+depth*1.25))
        wd = max(1,int(9/z))
        ox = (depth-2)*w*0.10; oy = (depth-2)*h*0.05
        step = w*0.115*z
        # chords
        for k in range(-2, int(w/step)+3):
            x = k*step+ox
            dr.line([(x, -h), (x+h*1.35, h*2)], fill=alpha, width=wd)
            dr.line([(x+h*1.35, -h), (x, h*2)], fill=int(alpha*0.7), width=max(1,wd-2))
        # horizontals (booms)
        for k in range(-1,7):
            y = k*h*0.22*z + oy + h*0.06
            dr.line([(-w, y), (w*2, y)], fill=int(alpha*0.9), width=wd+1)
    arr = np.array(im).astype(float)/255.0
    arr = np.array(Image.fromarray((arr*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7)))/255.0
    yy,xx = np.mgrid[0:h,0:w].astype(float)
    # depth fog + light gradient
    fog = norm(np.exp(-((yy/h-0.15)**2)*2.2) + 0.4)
    lightgrad = norm((xx/w)*0.7 + (1-yy/h)*0.5 + norm(fbm(h,w,5,3,seed=9))*0.35)
    base = lightgrad*0.42 + 0.05
    v = np.clip(base + arr*fog*0.85, 0, 1)
    if tone=='steel':
        stops=[(0.0,(8,9,12)),(0.3,(26,30,38)),(0.55,(64,72,84)),(0.78,(132,142,156)),(1.0,(226,232,240))]
    else:
        stops=[(0.0,(7,8,14)),(0.32,(18,26,50)),(0.58,(34,66,140)),(0.8,(88,140,226)),(1.0,(226,238,255))]
    img = ramp(v,stops)*255
    img += grain_layer(h,w,5.5,seed=5)
    vg = 1-0.5*norm(((xx/w-0.5)**2+(yy/h-0.5)**2*1.2))
    img *= vg[...,None]
    save(img, path)

# ------------------------------------------------------------- 3. HV / PYLON
def hv_network(path):
    h,w = H,W
    yy,xx = np.mgrid[0:h,0:w].astype(float)
    sky = norm((1-yy/h)**1.5 + norm(fbm(h,w,6,3,seed=31))*0.28)
    stops=[(0.0,(10,11,16)),(0.3,(20,24,40)),(0.55,(46,44,78)),(0.75,(128,72,74)),(0.9,(214,120,74)),(1.0,(255,206,150))]
    img = ramp(sky,stops)*255
    im = Image.new('L',(w,h),0); dr = ImageDraw.Draw(im)
    def pylon(cx, scale, alpha):
        top = h*(0.92-0.62*scale); base = h*0.99
        halfb = w*0.075*scale; halft = w*0.020*scale
        L=[(cx-halfb,base),(cx-halft,top)]; R=[(cx+halfb,base),(cx+halft,top)]
        wdt = max(2,int(7*scale))
        dr.line(L, fill=alpha, width=wdt); dr.line(R, fill=alpha, width=wdt)
        n=13
        for i in range(n):
            t0=i/n; t1=(i+1)/n
            def pt(side,t): 
                a=L if side==0 else R
                return (a[0][0]+(a[1][0]-a[0][0])*t, a[0][1]+(a[1][1]-a[0][1])*t)
            dr.line([pt(0,t0),pt(1,t1)], fill=int(alpha*0.85), width=max(1,wdt-3))
            dr.line([pt(1,t0),pt(0,t1)], fill=int(alpha*0.85), width=max(1,wdt-3))
            if i%4==0: dr.line([pt(0,t0),pt(1,t0)], fill=int(alpha*0.9), width=max(1,wdt-2))
        # cross arms
        for k,ty in enumerate([0.62,0.78,0.92]):
            y = base+(top-base)*ty; arm = w*0.085*scale*(1-k*0.16)
            dr.line([(cx-arm,y),(cx+arm,y)], fill=alpha, width=max(2,wdt-1))
            for s in (-1,1):
                dr.line([(cx+s*arm,y),(cx+s*arm*0.28,y-h*0.045*scale)], fill=int(alpha*0.8), width=max(1,wdt-3))
                dr.ellipse([cx+s*arm-4*scale,y,cx+s*arm+4*scale,y+16*scale], fill=int(alpha*0.9))
        return [(cx-w*0.085*scale, base+(top-base)*0.62), (cx+w*0.085*scale, base+(top-base)*0.62),
                (cx-w*0.071*scale, base+(top-base)*0.78), (cx+w*0.071*scale, base+(top-base)*0.78)]
    specs=[(w*0.14,1.0,235),(w*0.52,0.66,150),(w*0.80,0.44,95),(w*1.02,0.30,60)]
    anchors=[pylon(*s) for s in specs]
    # catenary conductors between pylons
    for i in range(len(anchors)-1):
        a,b = anchors[i], anchors[i+1]
        alpha = int(150/(1+i*0.9))
        for j in range(4):
            x0,y0 = a[j]; x1,y1 = b[j]
            pts=[]
            for t in np.linspace(0,1,60):
                sag = math.sin(t*math.pi)*h*0.05*(1-i*0.2)
                pts.append((x0+(x1-x0)*t, y0+(y1-y0)*t+sag))
            dr.line(pts, fill=alpha, width=max(1,3-i))
    arr = np.array(im.filter(ImageFilter.GaussianBlur(0.6))).astype(float)/255.0
    ink = np.array([9,9,13],dtype=float)
    img = img*(1-arr[...,None]*0.94) + ink*(arr[...,None]*0.94)
    # atmospheric haze near ground
    haze = np.exp(-((1-yy/h)*3.0))*0.5
    img = img*(1-haze[...,None]*0.5) + np.array([196,120,86])*haze[...,None]*0.5
    img += grain_layer(h,w,6,seed=8)
    vg = 1-0.45*norm(((xx/w-0.5)**2+(yy/h-0.55)**2*1.1))
    img *= vg[...,None]
    save(img, path)

# -------------------------------------------------------------- 4. THERMOGRAM
def thermogram(path):
    h,w = H,W
    yy,xx = np.mgrid[0:h,0:w].astype(float)
    base = norm(fbm(h,w,6,3,seed=77))*0.5
    heat = np.zeros((h,w))
    spots=[(0.30,0.42,0.09,1.0),(0.62,0.30,0.055,0.85),(0.74,0.66,0.07,0.72),(0.44,0.74,0.045,0.6),(0.16,0.66,0.035,0.5)]
    for cx,cy,r,amp in spots:
        d=np.sqrt(((xx/w-cx))**2+((yy/h-cy)*0.72)**2)
        heat += amp*np.exp(-(d/r)**1.5)
    # busbar / cable structures conducting heat
    for i,(y0,th,amp) in enumerate([(0.30,0.020,0.55),(0.44,0.014,0.42),(0.58,0.017,0.5)]):
        band = np.exp(-((yy/h-y0)/th)**2)
        heat += band*amp*(0.45+0.55*norm(fbm(h,w,4,6,seed=100+i)))
    v = norm(base*0.55 + heat)
    v = np.clip(v,0,1)**0.9
    stops=[(0.0,(4,4,20)),(0.18,(28,10,72)),(0.36,(96,18,110)),(0.54,(178,40,86)),(0.72,(238,102,36)),(0.88,(252,186,42)),(1.0,(255,250,214))]
    img = ramp(v,stops)*255
    img *= (1+0.022*np.sin(yy*math.pi*0.85))[...,None]
    img += grain_layer(h,w,4.5,seed=12)
    save(img, path)

# ------------------------------------------------------------- 5. WELD SPARKS
def weld(path):
    h,w = H,W
    yy,xx = np.mgrid[0:h,0:w].astype(float)
    cx,cy = w*0.34, h*0.58
    d = np.sqrt(((xx-cx)/w)**2+((yy-cy)/h*1.7)**2)
    v = np.exp(-d*11)*1.6 + np.exp(-d*3.0)*0.4
    im = Image.new('L',(w,h),0); dr = ImageDraw.Draw(im)
    r = np.random.default_rng(5)
    for _ in range(420):
        a = r.uniform(-math.pi*0.95, math.pi*0.35)
        ln = r.uniform(0.02,0.30)**1.5*w*1.6
        x,y = cx,cy; pts=[(x,y)]
        seg = max(3,int(ln/16))
        vx,vy = math.cos(a), math.sin(a)
        for s in range(seg):
            t=(s+1)/seg
            x += vx*ln/seg; y += vy*ln/seg + (t**2)*ln*0.16
            x += r.normal(0,ln*0.012)
            pts.append((x,y))
        dr.line(pts, fill=int(r.uniform(110,255)), width=1 if r.random()<0.7 else 2)
    sp = np.array(im.filter(ImageFilter.GaussianBlur(0.8))).astype(float)/255.0
    v = norm(v + sp*0.85)
    stops=[(0.0,(5,5,8)),(0.2,(20,14,14)),(0.42,(92,28,14)),(0.6,(212,74,18)),(0.78,(255,158,50)),(1.0,(255,250,228))]
    img = ramp(v,stops)*255
    img += grain_layer(h,w,6,seed=15)
    vg = 1-0.5*norm(((xx/w-0.42)**2+(yy/h-0.5)**2))
    img *= vg[...,None]
    save(img, path)

# ------------------------------------------------------------------ 6. GRAIN
def grain_tile(path, size=150, amount=26, alpha_base=255):
    r = np.random.default_rng(99)
    n = r.normal(128, amount, (size,size))
    a = np.abs(n-128)/amount*70
    rgba = np.zeros((size,size,4))
    rgba[...,0]=rgba[...,1]=rgba[...,2]=np.clip(n,0,255)
    rgba[...,3]=np.clip(a,0,120)
    Image.fromarray(rgba.astype(np.uint8)).save(path, optimize=True)
    print('  ->', path, f"{os.path.getsize(path)/1024:.0f}KB")

# ------------------------------------------------------------- 7. PAPER (site B)
def paper(path, size=900):
    h=w=size
    fib = norm(fbm(h,w,6,5,seed=200))
    fine = norm(fbm(h,w,3,60,seed=201))
    v = np.clip(0.82+fib*0.10+fine*0.08,0,1)
    stops=[(0.0,(228,224,214)),(0.5,(242,239,231)),(1.0,(252,250,245))]
    img = ramp(v,stops)*255
    img += np.random.default_rng(4).normal(0,2.6,(h,w,1))
    save(img, path)

def duotone_plate(path, kind, c_lo=(14,16,24), c_hi=(244,241,234), accent=None):
    """light editorial technical plates for site B"""
    h,w = 1200, 1600
    yy,xx = np.mgrid[0:h,0:w].astype(float)
    if kind=='truss':
        im = Image.new('L',(w,h),0); dr=ImageDraw.Draw(im)
        for depth in range(3):
            z=0.7+depth*0.5; a=int(230/(1+depth*1.4)); wd=max(1,int(7/z))
            oy=depth*h*0.10
            for k in range(-1,9):
                x=k*w*0.135*z
                dr.line([(x,h*0.86-oy),(x+w*0.09,h*0.24-oy)],fill=a,width=wd)
                dr.line([(x+w*0.09,h*0.86-oy),(x,h*0.24-oy)],fill=int(a*0.75),width=max(1,wd-2))
            dr.line([(-w,h*0.24-oy),(w*2,h*0.24-oy)],fill=a,width=wd+1)
            dr.line([(-w,h*0.86-oy),(w*2,h*0.86-oy)],fill=a,width=wd+1)
        m=np.array(im.filter(ImageFilter.GaussianBlur(0.7))).astype(float)/255
    elif kind=='coil':
        im = Image.new('L',(w,h),0); dr=ImageDraw.Draw(im)
        cx,cy=w*0.5,h*0.5
        for i in range(26):
            rr=(i+2)*w*0.017
            for turn in range(3):
                yo=(turn-1)*h*0.16
                bb=[cx-rr,cy-rr*0.34+yo,cx+rr,cy+rr*0.34+yo]
                dr.ellipse(bb, outline=int(210-i*5), width=3)
        for i in range(9):
            x=cx-w*0.20+i*w*0.05
            dr.line([(x,cy-h*0.34),(x,cy+h*0.34)],fill=110,width=2)
        m=np.array(im.filter(ImageFilter.GaussianBlur(0.8))).astype(float)/255
    else: # 'circuit'
        im = Image.new('L',(w,h),0); dr=ImageDraw.Draw(im)
        r=np.random.default_rng(33); gx,gy=26,20
        for i in range(gy):
            for j in range(gx):
                x=j*w/gx; y=i*h/gy
                if r.random()<0.55: dr.line([(x,y),(x+w/gx,y)],fill=int(r.uniform(90,200)),width=2)
                if r.random()<0.42: dr.line([(x,y),(x,y+h/gy)],fill=int(r.uniform(90,200)),width=2)
                if r.random()<0.12: dr.ellipse([x-5,y-5,x+5,y+5],outline=220,width=2)
        m=np.array(im.filter(ImageFilter.GaussianBlur(0.6))).astype(float)/255
    grad = norm((xx/w)*0.5+(1-yy/h)*0.5+norm(fbm(h,w,4,3,seed=55))*0.3)
    v = np.clip(0.90-grad*0.16-m*0.86,0,1)
    stops=[(0.0,c_lo),(0.55,(120,126,138) if accent is None else accent),(1.0,c_hi)]
    img=ramp(v,stops)*255
    img += np.random.default_rng(6).normal(0,3.0,(h,w,1))
    save(img,path)

A='site-a-forge/assets'; B='site-b-blueprint/assets'
os.makedirs(A,exist_ok=True); os.makedirs(B,exist_ok=True)
print('SITE A')
arc_field(f'{A}/arc-field.jpg')
lattice(f'{A}/steel-lattice.jpg','steel')
hv_network(f'{A}/hv-network.jpg')
thermogram(f'{A}/thermogram.jpg')
weld(f'{A}/weld.jpg')
lattice(f'{A}/lattice-blue.jpg','blue')
grain_tile(f'{A}/grain.png')
print('SITE B')
paper(f'{B}/paper.png')
grain_tile(f'{B}/grain.png', amount=18)
duotone_plate(f'{B}/plate-truss.jpg','truss', c_lo=(16,20,34), accent=(90,104,132))
duotone_plate(f'{B}/plate-coil.jpg','coil', c_lo=(30,14,18), accent=(150,88,88))
duotone_plate(f'{B}/plate-circuit.jpg','circuit', c_lo=(14,22,44), accent=(78,104,168))
print('done')
