#!/usr/bin/env python
# encoding: utf-8

from flask_wtf import FlaskForm
# importing flask.ext.wtf is deprecated, use flask_wtf instead.
# FlaskWTFDeprecationWarning: "flask_wtf.Form" has been renamed to "FlaskForm" and will be removed in 1.0.
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import TextField, TextAreaField, BooleanField, StringField, SubmitField, HiddenField
from wtforms.validators import Required, Length
from app import files

class LoginForm(FlaskForm):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = True)

class EditForm(FlaskForm):
    nickname = StringField('nickname', validators=[Required()])
    create_group_name = StringField('create_group_name')
    join_group_name = StringField('join_group_name')
    about_me = TextAreaField('about_me', validators=[Length(min=0, max=140)])

class UploadForm(FlaskForm):
    file = FileField(validators=[
        FileAllowed(files, u'只能上传媒体文件！'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')

class SearchForm(FlaskForm):
	search_str = StringField('search_str', validators=[Required()])