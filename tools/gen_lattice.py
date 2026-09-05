import numpy as np, math, os
from PIL import Image, ImageFilter, ImageDraw
exec(open('tools/gen_assets.py').read().split("A='site-a-forge/assets'")[0])

def truss_corridor(path, tone='steel'):
    """Perspective steel corridor: real vanishing point, depth fog + DOF."""
    h,w = H,W
    S=2
    vx, vy = w*0.66, h*0.44          # vanishing point
    layers=[]                         # (mask, depth 0=near .. 1=far)
    NZ=9
    for k in range(NZ):
        z = 0.30 + k*0.42             # distance
        s = 1.0/z
        im = Image.new('L',(w*S,h*S),0); dr=ImageDraw.Draw(im)
        lw = max(2,int(16*s*S))
        # rectangular portal frame at this depth, centred on VP
        pw, ph = w*0.62*s, h*0.72*s
        l,r = vx-pw, vx+pw
        t,b = vy-ph, vy+ph
        def P(x,y): return (x*S,y*S)
        # top & bottom booms
        dr.line([P(l,t),P(r,t)], fill=235, width=lw)
        dr.line([P(l,b),P(r,b)], fill=235, width=lw)
        dr.line([P(l,t),P(l,b)], fill=200, width=lw)
        dr.line([P(r,t),P(r,b)], fill=200, width=lw)
        # inner chord
        ih = ph*0.34
        dr.line([P(l,vy-ih),P(r,vy-ih)], fill=150, width=max(1,lw-int(2*S)))
        dr.line([P(l,vy+ih),P(r,vy+ih)], fill=150, width=max(1,lw-int(2*S)))
        # zig-zag web between booms (top band and bottom band)
        n = 9
        for band in ((t, vy-ih),(vy+ih, b)):
            y0,y1 = band
            for i in range(n):
                x0 = l + (r-l)*i/n; x1 = l + (r-l)*(i+1)/n
                dr.line([P(x0,y0),P(x1,y1)], fill=190, width=max(1,lw-int(2*S)))
                dr.line([P(x0,y1),P(x1,y0)], fill=160, width=max(1,lw-int(2*S)))
        layers.append((np.array(im.resize((w,h),Image.LANCZOS)).astype(float)/255.0, k/(NZ-1)))
    # longitudinal stringers running to the vanishing point
    im = Image.new('L',(w*S,h*S),0); dr=ImageDraw.Draw(im)
    for k in range(NZ-1):
        z0=0.30+k*0.42; z1=0.30+(k+1)*0.42
        for sx,sy in [(-1,-1),(1,-1),(-1,1),(1,1),(-1,-.34),(1,-.34),(-1,.34),(1,.34)]:
            a=(vx+sx*w*0.62/z0, vy+sy*h*0.72/z0); b=(vx+sx*w*0.62/z1, vy+sy*h*0.72/z1)
            dr.line([(a[0]*S,a[1]*S),(b[0]*S,b[1]*S)], fill=int(210/(1+k*.55)), width=max(2,int(14/z0*S)))
    stringers = np.array(im.resize((w,h),Image.LANCZOS)).astype(float)/255.0

    yy,xx = np.mgrid[0:h,0:w].astype(float)
    acc = np.zeros((h,w))
    for m,d in layers:
        blurpx = 3.4*max(0.0, 0.26-d)*10 + 0.6      # near frames slightly out of focus
        if blurpx > 0.6:
            m = np.array(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blurpx)))/255.0
        acc = np.maximum(acc, m*(1.0-d*0.48))
    acc = np.maximum(acc, stringers*0.95)
    # light: bright at the vanishing point, falling off outward
    dvp = np.sqrt(((xx-vx)/w)**2+((yy-vy)/h)**2)
    key = np.exp(-dvp*1.75)
    haze = norm(fbm(h,w,6,3,seed=61))
    base = 0.07 + key*0.34 + haze*0.13
    v = np.clip(base + acc*(0.52+key*0.72), 0, 1)
    if tone=='steel':
        stops=[(0.0,(7,8,11)),(0.26,(21,25,32)),(0.52,(58,66,78)),(0.76,(126,137,152)),(1.0,(228,234,242))]
    else:
        stops=[(0.0,(6,8,14)),(0.28,(16,24,48)),(0.54,(32,62,132)),(0.78,(86,136,222)),(1.0,(226,238,255))]
    img = ramp(v,stops)*255
    img += grain_layer(h,w,5.5,seed=5)
    vg = 1-0.52*norm(((xx/w-0.62)**2+(yy/h-0.48)**2*1.15))
    img *= vg[...,None]
    save(img, path)

truss_corridor('site-a-forge/assets/steel-lattice.jpg','steel')
truss_corridor('site-a-forge/assets/lattice-blue.jpg','blue')
