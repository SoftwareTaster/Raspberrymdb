#!/usr/bin/env python
# encoding: utf-8

import os
from flask import Flask
from flask_login import LoginManager # importing flask.ext.login is deprecated, use flask_login instead.
from flask_openid import OpenID # importing flask.ext.openid is deprecated, use flask_openid instead.
from flask_sqlalchemy import SQLAlchemy # importing flask.ext.sqlalchemy is deprecated, use flask_sqlalchemy instead.
from flask_uploads import UploadSet, configure_uploads, IMAGES, AUDIO, patch_request_class
from config import basedir

VIDEO = ('mp4', 'ogg', 'avi')

app = Flask(__name__) # 创建应用对象
app.config.from_object('config') # 告诉Flask去读取以及使用配置文件

# app.config['UPLOADED_PHOTO_DEST'] = os.getcwd() # RuntimeError: no destination for set photos???
app.config['UPLOADS_DEFAULT_DEST'] = os.path.join(os.path.join(os.getcwd(), 'app'), 'static') # 配置文件上传到的路径
# app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES # 限制上传文件的类型

files = UploadSet('files', IMAGES + AUDIO + VIDEO) # 实例化UploadSet类创建一个set，photos代表已经保存的文件
configure_uploads(app, files) # 传入当前应用实例和set以注册并完成相应的配置
patch_request_class(app, 32 * 1024 * 1024)  # 传入应用实例和大小，默认是16MB的大小

track_modifications = app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
# FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future. Set it to True or False to suppress this warning.
# SQLALCHEMY_TRACK_MODIFICATIONS：如果设置成True，Flask-SQLAlchemy将会追踪对象的修改并且发送信号，这需要额外的内存，如果不必要的可以禁用它

db = SQLAlchemy(app) # 初始化数据库

lm = LoginManager()
lm.init_app(app) # 初始化LoginManager
lm.login_view = 'login' # 指定哪个视图允许用户登录
oid = OpenID(app, os.path.join(basedir, 'tmp')) # 提供存储文件的临时文件夹

from app import views, models # 导入视图和模型