#!/usr/bin/env python
# encoding: utf-8

from app import db, models

Group = models.Group
User = models.User
Media = models.Media

# User # <class 'flask_sqlalchemy.model.DefaultMeta'> # can join
# User.groups # <class 'sqlalchemy.orm.attributes.InstrumentedAttribute'> # can join
# .all() # <type 'list'> # can not join

users = User.query.all() # [<User u'zbc'>, <User u'mjm'>]
# users = User.query # <class 'flask_sqlalchemy.BaseQuery'> # can not join
# SELECT user.id AS user_id, user.nickname AS user_nickname, user.email AS user_email, user.about_me AS user_about_me, user.last_seen AS user_last_seen
# FROM user

user = users[1] # <User u'mjm'>

groups = user.groups.all() # [<Group u'ss'>, <Group u'ssr'>]
# groups = user.groups # <class 'flask_sqlalchemy.BaseQuery'> # can not join
# SELECT "group".id AS group_id, "group".nickname AS group_nickname
# FROM "group", inthe
# WHERE ? = inthe.user_id AND "group".id = inthe.group_id

groups = user.groups.subquery() # <class 'sqlalchemy.sql.selectable.Alias'>
# SELECT "group".id, "group".nickname
# FROM "group", inthe
# WHERE :param_1 = inthe.user_id AND "group".id = inthe.group_id

# users = User.query.join(groups, User.id==groups.c.id).all() # [<User u'zbc'>, <User u'mjm'>] # WRONG!!!
# users = User.query.join(groups, User.id==groups.c.id) # <class 'flask_sqlalchemy.BaseQuery'>
# SELECT user.id AS user_id, user.nickname AS user_nickname, user.email AS user_email, user.about_me AS user_about_me, user.last_seen AS user_last_seen
# FROM user JOIN (SELECT "group".id AS id, "group".nickname AS nickname
# FROM "group", inthe
# WHERE ? = inthe.user_id AND "group".id = inthe.group_id) AS anon_1 ON user.id = anon_1.id

users = User.query.filter(User.groups.any(Group.users.contains(user))).all()

print(users)
print(type(users))