from PIL import Image, ImageDraw,ImageFont
import os

filename = "C:\\Users\\lenovo\\Desktop\\car.mp4"
uploader = "ZengBenChong"
out_path = "C:\\Users\\lenovo\\Desktop\\watermark_video\\"

watermark = Image.new('RGBA', (300,50), (0,0,0,0))
d = ImageDraw.Draw(watermark)
fnt = ImageFont.truetype("C:\\Windows\\fonts\\Tahoma.ttf", 30)
d.text( (0, 0), uploader, font=fnt, fill=(150,150,150,200) )
shortname = filename.split('\\')[-1] #Linux中使用/
purename = shortname.split('.')[0]
watermarkname = out_path + purename + '.png'
watermark.save(watermarkname)

comm = 'ffmpeg -i ' + filename + ' -i ' + watermarkname + ' -filter_complex overlay=30:10 ' \
	+ out_path + shortname + ' -y'
os.system(comm)
comm = 'del ' + watermarkname #Linux中使用rm
os.system(comm)