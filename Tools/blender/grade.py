from PIL import Image, ImageFilter, ImageEnhance, ImageStat
import glob, os, sys
U='/mnt/user-data/uploads/'
src={
 'Rat':'cartoon+mouse+3d+model/*.fbm/*basecolor*',
 'Pigeon':'bird+cartoon+3d+model/*.fbm/*basecolor*',
 'Pizza':'pizza+slice+3d+model/*.fbm/*BaseColor*',
 'HotDog':'hot+dog+3d+model/*.fbm/*basecolor*',
 'Soda':'red+soda+can+3d+model/*.fbm/*basecolor*',
 'Cheesecake':'strawberry+cheesecake+3d+model/*.fbm/*basecolor*'}
for k,g in src.items():
    f=glob.glob(U+g)[0]
    im=Image.open(f).convert('RGB')
    if im.size[0]>1024: im=im.resize((1024,1024),Image.LANCZOS)
    # flatten fine detail -> cartoon look
    im=im.filter(ImageFilter.MedianFilter(5))
    v=ImageStat.Stat(im.convert('L')).mean[0]/255
    if v<0.55: im=ImageEnhance.Brightness(im).enhance(min(1.45,0.6/max(v,0.2)))
    sat={'Rat':1.05,'Pigeon':1.1}.get(k,1.25)
    im=ImageEnhance.Color(im).enhance(sat)
    im=ImageEnhance.Contrast(im).enhance(1.08)
    im=im.quantize(colors=48,method=Image.Quantize.MEDIANCUT).convert('RGB').filter(ImageFilter.SMOOTH)
    if k=='Pizza' and os.path.exists('out/T_Pizza_BaseColor.png'): continue
    im.save(f'out/T_{k}_BaseColor.png')
    print(k, round(v,2))
