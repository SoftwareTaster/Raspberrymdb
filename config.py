#!/usr/bin/env python
# encoding: utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True # 激活跨站点请求伪造保护，使得你的应用程序更安全些
SECRET_KEY = 'you-will-never-guess' # 建立一个加密的令牌，用于验证一个表单

OPENID_PROVIDERS = [
    # { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    # { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    # { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    # { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    # { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }, # 定义一个 OpenID 提供者的列表
    { 'name': 'OPENID', 'url': 'http://<username>.openid.org.cn/'}] # for http://www.openid.org.cn/

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') # 数据库文件的路径
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository') # 是文件夹，我们将会把SQLAlchemy-migrate数据文件存储在这里