#该脚本可以根据图片大小自动调节水印文字的大小，而且水印永远居中显示
from PIL import Image, ImageDraw,ImageFont

filename = "C:/Users/lenovo/Desktop/yizhong.jpg"
uploader = "Zeng"
out_path = "C:/Users/lenovo/Desktop/watermark_pic/"

im = Image.open(filename).convert('RGBA')
width,height = im.size
fntlen = len(uploader)
fntsize = int(min(width,height)/4)
fnt = ImageFont.truetype("C:/Windows/fonts/Tahoma.ttf", fntsize)
watermark = Image.new('RGBA', im.size, (0,0,0,0))
d = ImageDraw.Draw(watermark)
d.text( ( (width-0.55*fntlen*fntsize)/2, (height-1.5*fntsize)/2), uploader, font=fnt, fill=(255,255,255,255) )
out = Image.alpha_composite(im, watermark)
shortname = filename.split('/')[-1]
out.save(out_path+shortname)