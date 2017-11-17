#!/usr/bin/env python
# encoding: utf-8

import imageio
imageio.plugins.ffmpeg.download()

import os
from PIL import Image
from moviepy.editor import VideoFileClip

mydir = 'D:\\Program\\ffmpeg-20171111-3af2bf0-win64-static\\bin'
os.environ["PATH"]= mydir + ";" + os.environ["PATH"]

def commEx(comm):
	print(comm)
	os.system(comm)
def format(name):
	filePath = os.path.join(os.getcwd(), 'app\\static\\files\\')
	# filePath = "C:\\Users\\lenovo\\Desktop\\files\\"
	scriptPath = os.path.join(os.getcwd(), 'app\\')
	# scriptPath = "C:\\Users\\lenovo\\Desktop\\"

	pureName = name.split(".")[0]
	fileFormat = name.split(".")[-1].lower() #为了避免匹配错误，统一转换成小写
	fileName = filePath + name

	if fileFormat=="mp3":
		commEx( "ruby " + scriptPath +"extractMp3Cover.rb " + fileName )
	elif fileFormat=="wav":
		commEx( "ffmpeg -i " + fileName + " " + filePath + pureName + ".mp3 -y" )
		commEx( "del " + fileName ) #Linux中使用rm
	elif fileFormat=="png" or fileFormat=="bmp":
		pic = Image.open(fileName)
		pic.save(filePath+pureName+".jpg")
		commEx( "del " + fileName ) #Linux中使用rm
	elif fileFormat=="mp4" or fileFormat=="avi" or fileFormat=="mov" or fileFormat=="flv" or fileFormat=="rmvb" or fileFormat=="mkv":
		picName = filePath + "show_video/" + pureName + ".png"
		clip = VideoFileClip(fileName)
		cutTime = int(clip.duration/2)
		commEx( "ffmpeg -ss " + str(cutTime) + " -i " + fileName + " " + picName \
			+ " -y -r 1 -vframes 1 -an -vcodec mjpeg" )
		if fileFormat!="mp4":
			commEx( "ffmpeg -i " + fileName + " " + filePath + pureName + ".mp4 -y" )
			commEx( "del " + fileName ) #Linux中使用rm
