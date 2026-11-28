import onnxruntime as ort, numpy as np, sys
from PIL import Image, ImageFilter
m=ort.InferenceSession(sys.argv[1]); inp=m.get_inputs()[0].name
for src,dst,box in [('src/f_776.0.png','mm_open.png',(300,0,1000,720)),('src/f_761.5.png','mm_fist.png',(280,0,980,720)),('src/f_778.0.png','host_point.png',(300,40,1000,720))]:
    im=Image.open(src).convert('RGB').crop(box); W,H=im.size
    x=np.asarray(im.resize((320,320),Image.BICUBIC)).astype(np.float32)/255.
    x=(x-[0.485,0.456,0.406])/[0.229,0.224,0.225]; x=x.transpose(2,0,1)[None].astype(np.float32)
    d=m.run(None,{inp:x})[0][0,0]; d=(d-d.min())/(d.max()-d.min()+1e-8)
    a=Image.fromarray((d*255).astype(np.uint8)).resize((W,H),Image.BICUBIC)
    a=a.point(lambda v:0 if v<90 else (255 if v>170 else int((v-90)*255/80))).filter(ImageFilter.GaussianBlur(1))
    out=im.convert('RGBA'); out.putalpha(a); out.save(dst); print(dst,W,H)
