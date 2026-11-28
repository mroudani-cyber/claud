import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw
rng=np.random.default_rng(7)
def noise(w,h,scale):
    n=rng.random((h//scale+2,w//scale+2)).astype(np.float32)
    return np.asarray(Image.fromarray((n*255).astype(np.uint8)).resize((w,h),Image.BICUBIC)).astype(np.float32)/255
# paper 4800x3800
W,H=4800,3800
base=np.array([236,231,221],np.float32)
m=0.55*noise(W,H,400)+0.3*noise(W,H,90)+0.15*noise(W,H,18)
grain=rng.normal(0,1,(H,W)).astype(np.float32)
fib=np.asarray(Image.fromarray(((rng.random((H,W))>0.9985)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).resize((W,H))).astype(np.float32)/255
lum=(m-0.5)*14+grain*2.2-fib*25
img=np.clip(base[None,None,:]+lum[...,None]*np.array([1,1,1.08]),0,255).astype(np.uint8)
Image.fromarray(img).save('a/paper.jpg',quality=90)
# B&W print from frame 776.0 (face+hands)
src=Image.open('src/f_776.0.png').convert('L').crop((330,30,930,690))
src=ImageOps.autocontrast(src,cutoff=1); src=ImageEnhance.Contrast(src).enhance(1.25)
g=np.asarray(src).astype(np.float32)+rng.normal(0,7,(src.size[1],src.size[0]))
src=Image.fromarray(np.clip(g,0,255).astype(np.uint8)).convert('RGB')
bw,bh=src.size; pad=26; bot=96
pr=Image.new('RGB',(bw+2*pad,bh+pad+bot),(246,244,238)); pr.paste(src,(pad,pad))
pr.save('a/print.jpg',quality=92)
# host sticker with white outline
h=Image.open('host_point.png'); a=h.split()[3].point(lambda v:255 if v>128 else 0)
h.putalpha(a)
o=a.filter(ImageFilter.MaxFilter(23)).filter(ImageFilter.GaussianBlur(1.2))
st=Image.new('RGBA',h.size,(250,249,245,0)); st.putalpha(o)
st.alpha_composite(h); bbox=st.getbbox(); st.crop(bbox).save('a/host_sticker.png')
# stamp grunge mask (white=ink)
sw,sh=900,300
gm=0.6*noise(sw,sh,6)+0.4*noise(sw,sh,40)
mask=np.clip((gm-0.28)*3.2,0,1)
Image.fromarray((mask*255).astype(np.uint8)).save('a/grunge.png')
# tape
tw,th=260,74
t=Image.new('RGBA',(tw,th),(0,0,0,0)); d=ImageDraw.Draw(t)
pts=[(0,0)]+[(tw*i/12, rng.uniform(0,6)) for i in range(1,12)]+[(tw,0),(tw- rng.uniform(0,8),th/2),(tw,th)]+[(tw-tw*i/12, th-rng.uniform(0,6)) for i in range(1,12)]+[(0,th),(rng.uniform(0,8),th/2)]
d.polygon(pts,fill=(232,224,200,150)); t.save('a/tape.png')
print('ok')
