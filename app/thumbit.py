#!/usr/bin/env python
# encoding: utf-8

from PIL import Image
import os
import sys
import glob
import time

filepath = os.path.join(os.getcwd(), 'app\\static\\files\\')
thumbpath = os.path.join(os.getcwd(), 'app\\static\\files\\cover')

def make_thumb(name, size, option):
    """生成缩略图"""
    if option == 0:
        path = os.path.join(filepath, name)
    else:
        path = os.path.join(thumbpath, name)
    img = Image.open(path)
    width, height = img.size
    # 裁剪图片成正方形
    if width > height:
        delta = (width - height) / 2
        box = (delta, 0, width - delta, height)
        region = img.crop(box)
    elif height > width:
        delta = (height - width) / 2
        box = (0, delta, width, height - delta)
        region = img.crop(box)
    else:
        region = img

    # 缩放
    if option == 0:
        thumb = region.resize((size, size), Image.ANTIALIAS)
    else:
        thumb = img.resize(((width / height) * size, size), Image.ANTIALIAS)

    base, ext = os.path.splitext(os.path.basename(path))
    if option == 0:
        filename = os.path.join(thumbpath, '%s.jpg' % (base,))
    else:
        os.remove(path)
        filename = os.path.join(thumbpath, '%s.png' % (base,))
    print filename
    # 保存
    thumb.save(filename)

if __name__ == '__main__':
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    THUMB_PATH = os.path.join(ROOT_PATH, 'thumbs')
    if not os.path.exists(THUMB_PATH):
        os.makedirs(THUMB_PATH)

    # 生成缩略图
    files = glob.glob(os.path.join(ROOT_PATH, '*.jpg')) # like ['F:\\source\\Raspberrymdb\\app\\static\\files\\1_1.jpg']
    begin_time = time.clock()
    for file in files:
        make_thumb(file, THUMB_PATH, 300)
    end_time = time.clock()
    print ('make_thumb time:%s' % str(end_time - begin_time))