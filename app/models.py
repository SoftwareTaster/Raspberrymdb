#!/usr/bin/env python
# encoding: utf-8

from hashlib import md5
from app import db

inthe = db.Table('inthe',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)
havethe = db.Table('havethe',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('media_id', db.Integer, db.ForeignKey('media.id'))
)

class Group(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	nickname = db.Column(db.String(64), index = True, unique = True)
	users = db.relationship('User', secondary=inthe, backref=db.backref('groups', lazy='dynamic'))

	def __repr__(self):
		return '<Group %r>' % (self.nickname)


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    phone = db.Column(db.String(20), index = True, unique = True)
    level = db.Column(db.Integer) # 1 普通用户 2 媒体供应商
    medias = db.relationship('Media', secondary=havethe, backref=db.backref('owner', lazy='dynamic'))
    buymedias = db.relationship('BuyMedia', backref='buyer', lazy='dynamic')
    collectmedias = db.relationship('CollectMedia', backref='collector', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    # backref 是一个在 Address 类上声明新属性的简单方法
    # lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据

    def is_authenticated(self):
    # 方法应该只返回True，除非表示用户的对象因为某些原因不允许被认证
        return True
    def is_active(self):
    # 方法应该返回True，除非是用户是无效的，比如因为他们的账号是被禁止
        return True
    def is_anonymous(self):
    # 方法应该返回True，除非是伪造的用户不允许登录系统
        return False
    def get_id(self):
    # 方法应该以unicode格式返回一个用数据库生成的用户唯一的标识符
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size) # Email Hash: de5371642e4e588a6531185bc904d2e1

    def __repr__(self):
        return '<User %r>' % (self.nickname)


class Media(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100)) # the true name of media
    furl = db.Column(db.String(200)) # the flask url of media
    mtype = db.Column(db.String(40)) # media type
    privilege = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

    def __repr__(self): # 告诉Python如何打印这个类的对象
        return '<Media %r>' % (self.name) # 改成一对多


class BuyMedia(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	furl = db.Column(db.String(200))
	mtype = db.Column(db.String(40))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 改成多对多


class CollectMedia(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	furl = db.Column(db.String(200))
	mtype = db.Column(db.String(40))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 改成多对多