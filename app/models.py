#!/usr/bin/env python
# encoding: utf-8

from hashlib import md5
from app import db

inthe = db.Table('inthe',
    db.Column('group_id', db.Integer, db.ForeignKey('group.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    secretkey = db.Column(db.String(64), unique = True) # 群组的密钥，用户输入此密钥以加入群组
    users = db.relationship('User', secondary=inthe, backref=db.backref('groups', lazy='dynamic'))

    def __repr__(self):
        return '<Group %r>' % (self.nickname)


fav = db.Table('favorite',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('media_id', db.Integer, db.ForeignKey('media.id'))
)
buy = db.Table('purchase',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('media_id', db.Integer, db.ForeignKey('media.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) # 用户号
    level = db.Column(db.Integer) # 用户类型：1 普通用户 2 媒体供应商
    nickname = db.Column(db.String(64), index = True, unique = True) # 用户名
    email = db.Column(db.String(120), index = True, unique = True) # 用户信息之邮箱
    phone = db.Column(db.String(20), index = True, unique = True) # 用户信息之电话号码
    about_me = db.Column(db.String(140)) # 自我介绍
    last_seen = db.Column(db.DateTime) # 上次登录时间
    medias = db.relationship('Media', backref='owner', lazy='dynamic') # Only 1 # 一对多
    issues = db.relationship('Issue', backref='owner', lazy='dynamic') # Only 2 # 一对多
    favs = db.relationship('Media', secondary=fav, backref='favors', lazy='dynamic') # Only 1 # 多对多
    buys = db.relationship('Media', secondary=buy, backref='buyers', lazy='dynamic') # Only 1 # 多对多
    # backref 是一个在 Address 类上声明新属性的简单方法
    # lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据
    def is_authenticated(self): # 方法应该只返回True，除非表示用户的对象因为某些原因不允许被认证
        return True
    def is_active(self): # 方法应该返回True，除非是用户是无效的，比如因为他们的账号是被禁止
        return True
    def is_anonymous(self): # 方法应该返回True，除非是伪造的用户不允许登录系统
        return False
    def get_id(self): # 方法应该以unicode格式返回一个用数据库生成的用户唯一的标识符
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size) # Email Hash: de5371642e4e588a6531185bc904d2e1

    def __repr__(self):
        if self.level == 1: # 普通用户
            return '<User %r>' % (self.nickname)
        if self.level == 2: # 媒体供应商
            return '<Superuser %r>' % (self.nickname)


class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True) # 媒体号
    name = db.Column(db.String(100)) # the true name of media
    curl = db.Column(db.String(200)) # 媒体封面
    furl = db.Column(db.String(200)) # 真实媒体
    mtype = db.Column(db.String(40)) # media type
    privilege = db.Column(db.Integer) # 媒体可见程度：1 私人 2 群组 3 公开
    timestamp = db.Column(db.DateTime) # 媒体上传时间
    timestring = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    viewers = db.Column(db.Integer) # 浏览数量，仅在播放页面里计数

    def __repr__(self): # 告诉Python如何打印这个类的对象
        return '<Media %r>' % (self.name) # 改成一对多！实际拥有者只有一个，要他允许才能从媒体库中将其删除。


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key = True) # 发行号
    name = db.Column(db.String(100)) # 媒体名字
    wurl = db.Column(db.String(200)) # 加了水印的媒体链接
    furl = db.Column(db.String(200)) # 未加水印的媒体链接
    mtype = db.Column(db.String(40)) # 媒体类型
    timestamp = db.Column(db.DateTime) # 媒体上传时间
    timestring = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    viewers = db.Column(db.Integer) # 浏览数量，仅在播放页面里计数

    def __repr__(self): # 告诉Python如何打印这个类的对象
        return '<Issue %r>' % (self.name) # 改成一对多！实际拥有者只有一个，要他允许才能从媒体库中将其删除。