#!/usr/bin/env python
# encoding: utf-8

#该脚本可以根据图片大小自动调节水印文字的大小，而且水印永远居中显示
from PIL import Image, ImageDraw,ImageFont
import os

def wvideo(name, username):
	path = 'app\\static\\files\\' + name
	pathp = 'app\\static\\files\\watermark\\'
	# filename = "C:/Users/lenovo/Desktop/yizhong.jpg"
	filename = os.path.join(os.getcwd(), path)
	# out_path = "C:/Users/lenovo/Desktop/watermark_pic/"
	out_path = os.path.join(os.getcwd(), pathp)
	uploader = username
	# filename = "C:\\Users\\lenovo\\Desktop\\car.mp4"
	# uploader = "ZengBenChong"
	# out_path = "C:\\Users\\lenovo\\Desktop\\watermark_video\\"

	watermark = Image.new('RGBA', (500,150), (0,0,0,0))
	d = ImageDraw.Draw(watermark)
	fnt = ImageFont.truetype("C:\\Windows\\fonts\\Tahoma.ttf", 100)
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


def wpic(name, username):
	path = 'app\\static\\files\\' + name
	pathp = 'app\\static\\files\\watermark\\'
	# filename = "C:/Users/lenovo/Desktop/yizhong.jpg"
	filename = os.path.join(os.getcwd(), path)
	# out_path = "C:/Users/lenovo/Desktop/watermark_pic/"
	out_path = os.path.join(os.getcwd(), pathp)
	uploader = username

	im = Image.open(filename).convert('RGBA')
	width,height = im.size
	fntlen = len(uploader)
	fntsize = int(min(width,height)/4)
	fnt = ImageFont.truetype("C:/Windows/fonts/Tahoma.ttf", fntsize)
	watermark = Image.new('RGBA', im.size, (0,0,0,0))
	d = ImageDraw.Draw(watermark)
	d.text( ( (width-0.55*fntlen*fntsize)/2, (height-1.5*fntsize)/2), uploader, font=fnt, fill=(255,255,255,255) )
	out = Image.alpha_composite(im, watermark)
	out = Image.merge('RGB', out.split()[:3])
	shortname = filename.split('\\')[-1]
	out.save(out_path+shortname)