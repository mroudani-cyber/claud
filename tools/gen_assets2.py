import numpy as np, math, os
from PIL import Image, ImageFilter, ImageDraw
exec(open('tools/gen_assets.py').read().split("A='site-a-forge/assets'")[0])

# --- improved arc field: molten pour, off-centre, less starburst
def arc_field2(path):
    h,w = H,W
    yy,xx = np.mgrid[0:h,0:w].astype(float)
    turb = norm(fbm(h,w,7,4,seed=91))
    v = np.zeros((h,w))
    for cx,cy,rx,ry,amp in [(0.30,0.56,0.24,0.16,1.0),(0.55,0.40,0.16,0.10,0.72),(0.78,0.62,0.13,0.09,0.5)]:
        d=np.sqrt(((xx/w-cx)/rx)**2+((yy/h-cy)/ry)**2)
        v += amp*np.exp(-d**1.35)
    v = v*(0.62+0.55*turb)
    flow = norm(fbm(h,w,5,2,seed=17))
    v += flow*np.exp(-np.abs(yy/h-0.55)*3.0)*0.30
    v = norm(v)**1.05
    stops=[(0.0,(6,6,9)),(0.20,(22,14,16)),(0.40,(84,24,18)),(0.58,(182,50,22)),(0.76,(240,124,40)),(0.92,(255,196,110)),(1.0,(255,244,214))]
    img = ramp(v,stops)*255
    img *= (1+0.022*np.sin(yy*math.pi*0.8))[...,None]
    img += grain_layer(h,w,6,seed=3)
    vg = 1-0.55*norm(((xx/w-0.45)**2*1.05+(yy/h-0.5)**2))
    img *= vg[...,None]
    save(img, path)

def ss_draw(w,h,fn,scale=2):
    im = Image.new('L',(w*scale,h*scale),0)
    fn(ImageDraw.Draw(im), scale)
    return im.resize((w,h), Image.LANCZOS)

def plate(path, kind, c_lo, accent, c_hi=(246,243,236)):
    h,w = 1200,1600
    yy,xx = np.mgrid[0:h,0:w].astype(float)
    if kind=='transformer':
        def f(dr,s):
            cx,cy = w*0.5*s, h*0.5*s
            # core: two limbs with windings, elevation view
            cw, ch = w*0.44*s, h*0.56*s
            dr.rectangle([cx-cw/2,cy-ch/2,cx+cw/2,cy+ch/2], outline=225, width=int(5*s))
            dr.rectangle([cx-cw/2+ int(w*0.075*s), cy-ch/2+int(h*0.10*s), cx+cw/2-int(w*0.075*s), cy+ch/2-int(h*0.10*s)], outline=150, width=int(3*s))
            for side in (-1,1):
                lx = cx + side*cw*0.29
                # winding coils as stacked rounded bars
                n=16
                for i in range(n):
                    y = cy-ch*0.30 + i*(ch*0.60/(n-1))
                    ww = w*0.085*s*(1.0 if 1<i<n-2 else 0.86)
                    dr.rounded_rectangle([lx-ww,y-int(7*s),lx+ww,y+int(7*s)], radius=int(7*s), outline=200, width=int(3*s))
                dr.line([(lx,cy-ch*0.30-int(20*s)),(lx,cy-ch/2-int(60*s))],fill=180,width=int(4*s))
                dr.ellipse([lx-int(16*s),cy-ch/2-int(96*s),lx+int(16*s),cy-ch/2-int(64*s)],outline=200,width=int(4*s))
            # bushings / HV terminals
            for k in (-1,0,1):
                bx = cx+k*cw*0.30
                for j in range(4):
                    r0=int((26-j*4)*s); yb=cy-ch/2-int((110+j*26)*s)
                    dr.ellipse([bx-r0*2.2,yb-r0*0.5,bx+r0*2.2,yb+r0*0.5],outline=170,width=int(3*s))
            # base + radiators
            dr.line([(cx-cw*0.62,cy+ch/2+int(24*s)),(cx+cw*0.62,cy+ch/2+int(24*s))],fill=210,width=int(6*s))
            for k in range(9):
                rx = cx-cw*0.56+k*(cw*1.12/8)
                dr.line([(rx,cy+ch/2),(rx,cy+ch/2+int(24*s))],fill=140,width=int(3*s))
        m = np.array(ss_draw(w,h,f).filter(ImageFilter.GaussianBlur(0.5))).astype(float)/255
    elif kind=='singleline':
        def f(dr,s):
            def L(a,b,fill=210,wd=4): dr.line([(a[0]*w*s,a[1]*h*s),(b[0]*w*s,b[1]*h*s)],fill=fill,width=int(wd*s))
            def C(p,r,fill=210,wd=4):
                dr.ellipse([(p[0]*w-r*w)*s,(p[1]*h-r*w)*s,(p[0]*w+r*w)*s,(p[1]*h+r*w)*s],outline=fill,width=int(wd*s))
            # incoming HV line
            L((0.03,0.22),(0.22,0.22)); 
            for k in range(3):  # disconnect switch
                pass
            L((0.22,0.22),(0.28,0.14),190,4); C((0.22,0.22),0.006,230,4); C((0.30,0.22),0.006,230,4)
            L((0.30,0.22),(0.44,0.22))
            # breaker
            dr.rectangle([0.44*w*s,0.19*h*s,0.50*w*s,0.25*h*s],outline=230,width=int(5*s))
            L((0.50,0.22),(0.62,0.22))
            # transformer (two circles)
            C((0.655,0.22),0.033,235,5); C((0.655,0.285),0.033,235,5)
            L((0.655,0.35),(0.655,0.46))
            # busbar
            L((0.12,0.46),(0.94,0.46),240,7)
            # feeders
            for i,fx in enumerate([0.20,0.33,0.46,0.59,0.72,0.85]):
                L((fx,0.46),(fx,0.58))
                dr.rectangle([(fx-0.018)*w*s,0.58*h*s,(fx+0.018)*w*s,0.635*h*s],outline=205,width=int(4*s))
                L((fx,0.635),(fx,0.74),185)
                if i%2==0:
                    C((fx,0.775),0.021,180,4)
                    L((fx-0.021,0.80),(fx+0.021,0.80),150,3)
                else:
                    dr.rectangle([(fx-0.026)*w*s,0.752*h*s,(fx+0.026)*w*s,0.812*h*s],outline=180,width=int(4*s))
                L((fx,0.83),(fx,0.87),130,3)
                L((fx-0.028,0.87),(fx+0.028,0.87),130,4)
                L((fx-0.016,0.888),(fx+0.016,0.888),120,3)
                L((fx-0.007,0.903),(fx+0.007,0.903),110,3)
        m = np.array(ss_draw(w,h,f).filter(ImageFilter.GaussianBlur(0.45))).astype(float)/255
    else: # truss elevation
        def f(dr,s):
            for depth,(alp,off,sc) in enumerate([(120,0.16,0.80),(200,0.0,1.0)]):
                top=(0.30+off)*h*s; bot=(0.76+off)*h*s
                wd=int((4+depth*3)*s)
                dr.line([(0,top),(w*s,top)],fill=alp,width=wd+int(2*s))
                dr.line([(0,bot),(w*s,bot)],fill=alp,width=wd+int(2*s))
                step=w*0.105*s*sc
                k=-1
                while k*step < w*s+step:
                    x=k*step
                    dr.line([(x,bot),(x+step,top)],fill=alp,width=wd)
                    dr.line([(x,top),(x+step,bot)],fill=int(alp*0.8),width=wd)
                    dr.line([(x,top),(x,bot)],fill=int(alp*0.55),width=max(1,wd-int(2*s)))
                    k+=1
                for k in range(0,20,2):
                    x=k*step*0.5
                    dr.ellipse([x-6*s,top-6*s,x+6*s,top+6*s],fill=alp)
                    dr.ellipse([x-6*s,bot-6*s,x+6*s,bot+6*s],fill=alp)
        m = np.array(ss_draw(w,h,f).filter(ImageFilter.GaussianBlur(0.5))).astype(float)/255
    grad = norm((xx/w)*0.45+(1-yy/h)*0.45+norm(fbm(h,w,4,3,seed=55))*0.28)
    v = np.clip(0.93-grad*0.14-m*0.88,0,1)
    img = ramp(v,[(0.0,c_lo),(0.5,accent),(1.0,c_hi)])*255
    img += np.random.default_rng(6).normal(0,3.0,(h,w,1))
    save(img,path)

A='site-a-forge/assets'; B='site-b-blueprint/assets'
arc_field2(f'{A}/arc-field.jpg')
plate(f'{B}/plate-truss.jpg','truss',(14,18,32),(96,110,138))
plate(f'{B}/plate-transformer.jpg','transformer',(38,12,16),(158,86,88))
plate(f'{B}/plate-singleline.jpg','singleline',(12,20,44),(74,102,168))
os.path.exists(f'{B}/plate-coil.jpg') and os.remove(f'{B}/plate-coil.jpg')
os.path.exists(f'{B}/plate-circuit.jpg') and os.remove(f'{B}/plate-circuit.jpg')
# paper as jpg (smaller)
im=Image.open(f'{B}/paper.png').resize((760,760),Image.LANCZOS); im.save(f'{B}/paper.jpg',quality=92,optimize=True)
os.remove(f'{B}/paper.png')
print('paper.jpg', os.path.getsize(f'{B}/paper.jpg')//1024,'KB')
