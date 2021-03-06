#!/usr/bin/env python
# encoding: utf-8

import os, sys
from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required # importing flask.ext.login is deprecated, use flask_login instead.
from flask_uploads import IMAGES, AUDIO
from app import app, db, lm, oid, files
from .forms import LoginForm, EditForm, UploadForm, SearchForm
from .models import User, Media, Group, Issue, Association
from datetime import datetime

from format import format
from watermarking import wpic, wvideo
from thumbit import make_thumb
from PIL import Image
import hashlib
import qrcode
import subprocess

AUDIOS = AUDIO
VIDEOS = ('mp4', 'ogg')

# F:\\source\\Raspberrymdb
filespath = os.path.join(os.getcwd(), 'app\\static\\files')
shortpath = os.path.join(os.getcwd(), 'app')
qrpath = os.path.join(filespath, 'qrcode')

def item2id(x):
    return x.id

@lm.user_loader
def load_user(id): # 从数据库加载用户，它将会被Flask-Login使用
    return User.query.get(int(id))

@app.before_request # 任何使用了before_request装饰器的函数在接收请求之前都会运行
def before_request():
    g.user = current_user
    # 全局变量current_user是被Flask-Login设置的
    # 另，在登录视图函数中我们检查g.user是为了决定用户是否已经登录，有了这个，即使在模版里所有请求将会访问到登录用户
    if g.user.is_authenticated: # 用来在数据库中更新用户最后一次的访问时间
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


# ## ②私人媒体页、③群组媒体页、④公开媒体页：
# @app.route('/backindex', methods = ['GET', 'POST'])
# @login_required # 确保了这页只被已经登录的用户看到
# # 如果未登录访问了一个作了login_required限制的view，那么Flask-Login会默认flash一条消息，并且将重定向到login的view
# # 如果你没有指定login的view，那么Flask-Login将会抛出一个401错误
# def backindex():
#     form = SearchForm()
#     flag = '1'
#     user = g.user
#     if form.validate_on_submit(): # searching
#         flag = form.whichblock.data
#         search_str = '%' + form.search_str.data + '%'
#         image_medias_1 = Media.query.filter(Media.owner.any(User.id==g.user.id)).filter(Media.privilege==1).filter(Media.mtype.in_(IMAGES)).filter(Media.name.like(search_str)).all()
#         audio_medias_1 = Media.query.filter(Media.owner.any(User.id==g.user.id)).filter(Media.privilege==1).filter(Media.mtype.in_(AUDIOS)).filter(Media.name.like(search_str)).all()
#         video_medias_1 = Media.query.filter(Media.owner.any(User.id==g.user.id)).filter(Media.privilege==1).filter(Media.mtype.in_(VIDEOS)).filter(Media.name.like(search_str)).all()
#         users = map(item2id, User.query.filter(User.groups.any(Group.users.contains(g.user))).all())
#         image_medias_2 = Media.query.filter(Media.owner.any(User.id.in_(users))).filter(Media.privilege.in_([2, 3])).filter(Media.mtype.in_(IMAGES)).filter(Media.name.like(search_str)).all()
#         audio_medias_2 = Media.query.filter(Media.owner.any(User.id.in_(users))).filter(Media.privilege.in_([2, 3])).filter(Media.mtype.in_(AUDIOS)).filter(Media.name.like(search_str)).all()
#         video_medias_2 = Media.query.filter(Media.owner.any(User.id.in_(users))).filter(Media.privilege.in_([2, 3])).filter(Media.mtype.in_(VIDEOS)).filter(Media.name.like(search_str)).all()
#         image_medias_3 = Media.query.filter(Media.privilege==3).filter(Media.mtype.in_(IMAGES)).filter(Media.name.like(search_str)).all()
#         audio_medias_3 = Media.query.filter(Media.privilege==3).filter(Media.mtype.in_(AUDIOS)).filter(Media.name.like(search_str)).all()
#         video_medias_3 = Media.query.filter(Media.privilege==3).filter(Media.mtype.in_(VIDEOS)).filter(Media.name.like(search_str)).all()
#     else: # is not searching
#         image_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.privilege==1).filter(Media.mtype.in_(IMAGES)).all()
#         audio_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.privilege==1).filter(Media.mtype.in_(AUDIOS)).all()
#         video_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.privilege==1).filter(Media.mtype.in_(VIDEOS)).all()
#         users = map(item2id, User.query.filter(User.groups.any(Group.users.contains(g.user))).all())
#         image_medias_2 = Media.query.filter(Media.owner.has(User.id.in_(users))).filter(Media.privilege.in_([2, 3])).filter(Media.mtype.in_(IMAGES)).all()
#         audio_medias_2 = Media.query.filter(Media.owner.has(User.id.in_(users))).filter(Media.privilege.in_([2, 3])).filter(Media.mtype.in_(AUDIOS)).all()
#         video_medias_2 = Media.query.filter(Media.owner.has(User.id.in_(users))).filter(Media.privilege.in_([2, 3])).filter(Media.mtype.in_(VIDEOS)).all()
#         image_medias_3 = Media.query.filter(Media.privilege==3).filter(Media.mtype.in_(IMAGES)).all()
#         audio_medias_3 = Media.query.filter(Media.privilege==3).filter(Media.mtype.in_(AUDIOS)).all()
#         video_medias_3 = Media.query.filter(Media.privilege==3).filter(Media.mtype.in_(VIDEOS)).all()
#     medias_1 = [image_medias_1, audio_medias_1, video_medias_1]
#     medias_2 = [image_medias_2, audio_medias_2, video_medias_2]
#     medias_3 = [image_medias_3, audio_medias_3, video_medias_3]
#     print flag
#     return render_template("index.html",
#         title = 'Home',
#         form = form,
#         flag = flag,
#         user = user,
#         medias1 = medias_1, medias2 = medias_2, medias3 = medias_3)


## 登录页：
@app.route('/login', methods = ['GET', 'POST']) # 参数告诉Flask这个视图函数接受GET和POST请求，如果不带参数的话，视图只接受GET请求
@oid.loginhandler # 告诉Flask-OpenID这是我们的登录视图函数
def login():
    if g.user is not None and g.user.is_authenticated:
    # 检查g.user是否被设置成一个认证用户，如果是的话将会被重定向到首页，这里的想法是如果是一个已经登录的用户的话，就不需要二次登录了
        return redirect(url_for('index'))
    form = LoginForm() # 实例化一个LoginForm对象
    if form.validate_on_submit(): # 如果它在表单提交请求中被调用，那么它将会收集所有的数据，对字段进行验证
        session['remember_me'] = form.remember_me.data # 一旦数据存储在会话对象中，在来自同一客户端的现在和任何以后的请求都是可用的
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
        # 触发用户使用Flask-OpenID认证，参数是用户在web表单提供的openid和我们从OpenID提供商得到的数据项列表
        # OpenID认证异步发生，如果认证成功的话，Flask-OpenID将会调用一个注册了oid.after_login装饰器的函数，如果失败的话，用户将会回到登陆页面

        # flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        # 闪现的消息将不会自动地出现在我们的页面上，我们的模板需要加入展示消息的内容
        # return redirect('/index')
        # 在我们的视图函数中我们用它重定向到前面已经完成的首页上，要注意地是，闪现消息将会显示即使视图函数是以重定向结束

    return render_template('xvlvtao/login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'][0])

@oid.after_login
def after_login(resp): # 参数resp包含了从OpenID提供商返回来的信息
    if resp.email is None or resp.email == "": # 我们需要一个合法的邮箱地址，因此不提供邮箱地址是不能登录的
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None: # 如果邮箱地址不在数据库中，我们认为是一个新用户，因此我们会添加一个新用户到数据库
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email, level=1)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session: # 从flask会话中加载remember_me值
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me) # 为了注册这个有效的登录
    return redirect(request.args.get('next') or url_for('index')) # 在next页没有提供的情况下，我们会重定向到首页，否则会重定向到next页


## 登出处理：
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('aboutus'))


# ## 编辑页：
# @app.route('/user/<nickname>')
# @login_required
# def user(nickname):
#     user = User.query.filter_by(nickname = nickname).first()
#     if user == None:
#         flash('User ' + nickname + ' not found.')
#         return redirect(url_for('index')) # ???
#     if user == g.user: # 自己访问有修改权限
#         image_medias = Media.query.filter(Media.owner.any(User.id==g.user.id)).filter(Media.mtype.in_(IMAGES)).all()
#         audio_medias = Media.query.filter(Media.owner.any(User.id==g.user.id)).filter(Media.mtype.in_(AUDIOS)).all()
#         video_medias = Media.query.filter(Media.owner.any(User.id==g.user.id)).filter(Media.mtype.in_(VIDEOS)).all()
#         medias = [image_medias, audio_medias, video_medias]
#         return render_template('user.html',
#             user = user,
#             medias = medias)
#     else: # 他人访问无修改权限
#         medias = []
#         return render_template('user.html',
#             user = user,
#             medias = medias)


# ## 配置页：
# @app.route('/edit', methods=['GET', 'POST'])
# @login_required
# def edit():
#     form = EditForm()
#     if form.validate_on_submit():
#         g.user.nickname = form.nickname.data
#         g.user.about_me = form.about_me.data
#         if form.create_group_name.data: # 创建群组
#             g.group = Group()
#             g.group.nickname = form.create_group_name.data
#             g.group.users.append(g.user)
#             db.session.add(g.group)
#         if form.join_group_name.data: # 加入群组
#             join_group = Group.query.filter(Group.nickname == form.join_group_name.data).all()
#             if join_group: # 群组存在
#                 join_group[0].users.append(g.user)
#                 db.session.add(join_group[0])
#             else: # 群组不存在
#                 flash('There is no such group name.')
#         db.session.add(g.user)
#         db.session.commit()
#         flash('Your changes have been saved.')
#         return redirect(url_for('edit'))
#     else:
#         form.nickname.data = g.user.nickname
#         form.about_me.data = g.user.about_me
#     groups = g.user.groups.all()
#     return render_template('edit.html', form=form, groups = groups)


def user_upload():
    for file in request.files.getlist('file'):
        filename = files.save(file, name = str(g.user.id) + '_' + str(len(g.user.medias.all()) + 1) + '.') # save uploaded medias in DIR`files` and get its name
        # file_url = files.url(filename) # This function gets the URL a file uploaded to this set would be accessed at # TMD it's address of source file
        format(filename) # change medias to the three format and save the covers
        filename = filename.replace('.png', '.jpg').replace('.bmp', '.jpg').replace('.gif', '.jpg').replace('.wav', '.mp3').replace('.avi', '.mp4').replace('.mkv', '.mp4') # ......
        g.media = Media()
        g.media.name = os.path.splitext(file.filename)[0] # the original name of media
        g.media.furl = url_for('static', filename='files/' + filename) # the storage path of media
        g.media.mtype = os.path.splitext(filename)[1][1:] # the type of media which is jpg and mp3 and mp4
        if g.media.mtype == 'jpg':
            make_thumb(filename, 1024, 0)
            cfilename = filename
        elif g.media.mtype == 'mp3':
            cfilename = filename.replace('.mp3', '.png')
        else: # 'mp4'
            make_thumb(filename.replace('.mp4', '.png'), 1920, 1)
            cfilename = filename.replace('.mp4', '.png')
        g.media.curl = url_for('static', filename='files/cover/' + cfilename)
        g.media.privilege = 2 # default is 'shared in group'
        g.media.timestamp = datetime.now()
        g.media.timestring = g.media.timestamp.strftime('%b %d %H:%M')
        g.media.user_id = g.user.id
        g.media.viewers = 0
        db.session.add(g.media)
        db.session.commit()
        g.user.medias.append(g.media)
        db.session.add(g.user)
        db.session.commit()
## 一般用户的上传页面：
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        if g.user.level == 1: # normal users
            user_upload()
        if g.user.level == 2:
            super_user_upload()
        # for file in request.files.getlist('file'):
        #     filename = files.save(file, name = str(g.user.id) + '_' + str(len(g.user.medias.all()) + 1) + '.')
        #     # file_url = files.url(filename) # This function gets the URL a file uploaded to this set would be accessed at. # 妈的是源文件的地址链接
        #     format(filename)
        #     filename = filename.replace('.png', '.jpg').replace('.bmp', '.jpg').replace('.wav', '.mp3').replace('.avi', '.mp4').replace('.mkv', '.mp4') # ......
        #     g.media = Media()
        #     g.media.name = os.path.splitext(file.filename)[0]
        #     g.media.furl = url_for('static', filename='files/' + filename)
        #     g.media.mtype = os.path.splitext(filename)[1][1:]
        #     g.media.privilege = 2 # default is 'shared in family'
        #     g.media.timestamp = datetime.utcnow()
        #     g.media.user_id = g.user.id
        #     db.session.add(g.media)
        #     db.session.commit()
        #     g.user.medias.append(g.media)
        #     db.session.add(g.user)
        #     db.session.commit()
    return render_template('xvlvtao/upload.html', form=form)
def super_user_upload():
    for file in request.files.getlist('file'):
        filename = files.save(file, name = str(g.user.id) + '_' + str(len(g.user.issues.all()) + 1) + '.')
        format(filename)
        filename = filename.replace('.png', '.jpg').replace('.bmp', '.jpg').replace('.gif', '.jpg').replace('.wav', '.mp3').replace('.avi', '.mp4').replace('.mkv', '.mp4') # ......
        if os.path.splitext(filename)[1][1:] == 'jpg':
            wpic(filename, g.user.nickname)
        if os.path.splitext(filename)[1][1:] == 'mp4':
            wvideo(filename, g.user.nickname)
        g.issue = Issue()
        g.issue.name = os.path.splitext(file.filename)[0]
        g.issue.furl = url_for('static', filename='files/' + filename)
        g.issue.mtype = os.path.splitext(filename)[1][1:]
        if g.issue.mtype == 'jpg':
            make_thumb(filename, 1024, 0)
            cfilename = filename
        elif g.issue.mtype == 'mp3':
            cfilename = filename.replace('.mp3', '.png')
        else: # 'mp4'
            make_thumb(filename.replace('.mp4', '.png'), 720, 1)
            cfilename = filename.replace('.mp4', '.png')
        g.issue.curl = url_for('static', filename='files/cover/' + cfilename)
        g.issue.wurl = url_for('static', filename='files/watermark/' + filename)
        if g.issue.mtype == 'mp3':
            g.issue.wurl = g.issue.furl
        g.issue.timestamp = datetime.now()
        g.issue.timestring = g.issue.timestamp.strftime('%b %d %H:%M')
        g.issue.user_id = g.user.id
        g.issue.viewers = 0
        g.issue.buyerno = 0
        g.issue.flag = 1
        g.issue.price = 6 # the default price is 6 yuan
        db.session.add(g.issue)
        db.session.commit()
        g.user.issues.append(g.issue)
        db.session.add(g.user)
        db.session.commit()
# ## 特殊用户的上传页面：
# @app.route('/supload', methods=['GET', 'POST']) # 提供商
# @login_required
# def supload_file():
#     form = UploadForm()
#     # if form.validate_on_submit():
#     #     for file in request.files.getlist('file'):
#     #         filename = files.save(file, name = str(g.user.id) + '_' + str(len(g.user.medias.all()) + 1) + '.')
#     #         # file_url = files.url(filename) # This function gets the URL a file uploaded to this set would be accessed at. # 妈的是源文件的地址链接
#     #         format(filename)
#     #         filename = filename.replace('.png', '.jpg').replace('.bmp', '.jpg').replace('.wav', '.mp3').replace('.avi', '.mp4').replace('.mkv', '.mp4') # ......
#     #         if os.path.splitext(filename)[1][1:] == 'jpg':
#     #             wpic(filename, g.user.nickname)
#     #         if os.path.splitext(filename)[1][1:] == 'mp4':
#     #             wvideo(filename, g.user.nickname)
#     #         g.media = Media()
#     #         g.media.name = os.path.splitext(file.filename)[0]
#     #         g.media.furl = url_for('static', filename='files/' + filename)
#     #         g.media.mtype = os.path.splitext(filename)[1][1:]
#     #         g.media.privilege = 2 # default is 'shared in family'
#     #         g.media.timestamp = datetime.utcnow()
#     #         g.media.user_id = g.user.id
#     #         db.session.add(g.media)
#     #         db.session.commit()
#     #         g.user.medias.append(g.media)
#     #         db.session.add(g.user)
#     #         db.session.commit()
#     return render_template('upload.html', form=form)


# ## 编辑页处理：
# @app.route('/control', methods=['GET', 'POST'])
# @login_required
# def control_file():
#     delete = Media.query.filter(Media.id.in_(request.args.getlist('delete'))).all()
#     if delete:
#         for x in delete:
#             g.user.medias.remove(x)
#             db.session.add(g.user)
#             db.session.commit()
#             db.session.delete(x)
#             db.session.commit()
#             os.remove(os.path.join(filespath, x.name))
#     else:
#         rename = Media.query.filter(Media.id.in_(request.args.getlist('rid'))).all()
#         if rename:
#             for (i, x) in enumerate(rename):
#                 x.name = request.args.getlist('rename')[i]
#                 db.session.add(x)
#             db.session.commit()
#         else:
#             for x in request.args.lists():
#                 privilege = Media.query.filter(Media.id == x[0]).all()
#                 privilege[0].privilege = x[1][0] # 1 私有 2 群组间共享 3 公有
#                 db.session.add(privilege[0])
#                 db.session.commit()
#     return redirect('/user/' + g.user.nickname)


# ## 请求：
# @app.route('/ask4', methods=['GET', 'POST'])
# @login_required
# def ask_for_file():
#     ask4 = Media.query.filter(Media.id == request.args.get('buywhat')).all()[0]
#     g.user.medias.append(ask4)
#     db.session.add(g.user)
#     db.session.commit()
#     return redirect(url_for('index'))


## 完善信息请求：
@app.route('/phone', methods=['GET', 'POST'])
@login_required
def set_phone():
    g.user.phone = request.args.get('phonenumber')
    g.user.nickname = request.args.get('nickname')
    g.user.about_me = request.args.get('about_me')
    db.session.add(g.user)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))


## 创建群组请求：
@app.route('/buildgroup', methods=['GET', 'POST'])
@login_required
def build_group():
    if request.args.get('groupname'):
        g.group = Group()
        g.group.nickname = request.args.get('groupname')
        print(request.args.get('groupname'))
        hash_md5 = hashlib.md5(g.group.nickname)
        g.group.secretkey = hash_md5.hexdigest()
        imm = qrcode.make(g.group.secretkey).resize((100, 100), Image.ANTIALIAS)
        qrname = os.path.join(qrpath, g.group.nickname) + '.bmp'
        imm.save(qrname)
        g.group.qrCode = url_for('static', filename='files/qrcode/' + os.path.split(qrname)[1])
        g.group.users.append(g.user)
        db.session.add(g.group)
        db.session.add(g.user)
        db.session.commit()
    return redirect(request.referrer or url_for('index'))


## 加入群组请求
@app.route('/uploadcode', methods=['GET', 'POST'])
@login_required
def upload_code():
    form = UploadForm()
    if form.validate_on_submit():
        img = request.files.get('file')
        filename = hashlib.md5(g.user.nickname).hexdigest()[:10]
        image = files.save(img, name=filename + '.')
        ipath = filespath + '\\' + image
        keyString = subprocess.check_output(["ZBar\\bin\\zbarimg", "-q", ipath])[8:]
        GetGroup = Group.query.filter(Group.secretkey == keyString.strip()).first()
        print(keyString.strip())
        print(GetGroup)
        if GetGroup:
            GetGroup.users.append(g.user)
            db.session.add(GetGroup)
            db.session.commit()
            os.remove(ipath)
            return redirect(url_for('index'))
        os.remove(ipath)
    return render_template('xvlvtao/upload-qrcode.html', form=form)


## 收藏请求：
@app.route('/likeit/<int:mid>/<int:which>', methods=['GET', 'POST'])
@login_required
def likeit(mid, which):
    if which == 1:
        if g.user.favs.query.filter(Media.id==mid):
            pass
        else:
            g.user.favs.append(Media.query.filter(Media.id==mid).first())
            db.session.add(g.user)
            db.session.commit()
    else:
        if g.user.ifavs.query.filter(Issue.id==mid):
            pass
        else:
            g.user.ifavs.append(Issue.query.filter(Issue.id==mid).first())
            db.session.add(g.user)
            db.session.commit()
    return redirect(request.referrer or url_for('index'))


## 购买请求：
@app.route('/buyit/<int:iid>', methods=['GET', 'POST'])
@login_required
def buyit(iid):
    if Association.query.filter(Association.buyer.has(User.id==g.user.id)).filter(Association.buy.has(Issue.id==iid)).all():
        pass
    else:
        a = Association(extra_privilege=1)
        a.buy = Issue.query.filter(Issue.id==iid).first()
        a.buyer = g.user
        db.session.add(a)
        db.session.commit()
    return redirect(request.referrer or url_for('index'))


## 编辑请求：
@app.route('/editit/<int:eid>', methods=['GET', 'POST']) # Only me!!!
@login_required
def editit(eid):
    if g.user.level == 1:
        g.media = Media.query.filter(Media.id==eid).first()
        if request.args.get('newname'):
            g.media.name = request.args.get('newname')
        if request.args.get('newintro'):
            g.media.about = request.args.get('newintro')
        if request.args.get('privilege'):
            g.media.privilege = 2
        else:
            g.media.privilege = 1
        db.session.add(g.media)
        db.session.commit()
    else: # g.user.level == 2
        g.issue = Issue.query.filter(Issue.id==eid).first()
        if request.args.get('newname'):
            g.issue.name = request.args.get('newname')
        if request.args.get('price'):
            g.issue.price = request.args.get('price')
        if request.args.get('newintro'):
            g.issue.about = request.args.get('newintro')
        db.session.add(g.issue)
        db.session.commit()
    return redirect(request.referrer or url_for('index'))


## 编辑请求：
@app.route('/Editit/<int:eid>', methods=['GET', 'POST'])
@login_required
def Editit(eid):
    g.association = Association.query.filter(Association.buyer.has(User.id==g.user.id)).filter(Association.buy.has(Issue.id==eid)).first()
    if request.args.get('privilege'):
        g.association.extra_privilege = 2
        print("sfg ")
    else:
        g.association.extra_privilege = 1
    db.session.add(g.association)
    db.session.commit()
    return redirect(request.referrer or url_for('index'))


def removeAll(*url):
    for u in url:
        thispath = os.path.join(shortpath, u[1:]).encode('utf-8')
        os.remove(thispath)
## 删除请求
@app.route('/deleteit/<int:did>', methods=['GET', 'POST'])
@login_required
def deleteit(did):
    if g.user.level == 1:
        removeOne = Media.query.filter(Media.id==did).first()
        url1=removeOne.curl
        url2=removeOne.furl
        g.user.medias.remove(removeOne)
        db.session.add(g.user)
        db.session.commit()
        db.session.delete(removeOne)
        db.session.commit()
        removeAll(url1, url2)
    else:
        removeOne = Issue.query.filter(Issue.id==did).first()
        url1=removeOne.curl
        url2=removeOne.furl
        url3=removeOne.wurl
        g.user.issues.remove(removeOne)
        db.session.add(g.user)
        db.session.commit()
        db.session.delete(removeOne)
        db.session.commit()
        if url2 == url3:
            removeAll(url1, url2)
        else:
            removeAll(url1, url2, url3)
    return redirect(request.referrer or url_for('index'))


## 取消收藏请求
@app.route('/nofavit/<int:did>/<int:which>', methods=['GET', 'POST'])
@login_required
def nofavit(did, which):
    if which == 1:
        removeOne = Media.query.filter(Media.id==did).first()
        g.user.favs.remove(removeOne)
        db.session.add(g.user)
        db.session.commit()
    else:
        removeOne = Issue.query.filter(Issue.id==did).first()
        g.user.ifavs.remove(removeOne)
        db.session.add(g.user)
        db.session.commit()
    return redirect(request.referrer or url_for('index'))


# 测试：
@app.route('/test')
def test():
    return redirect(url_for('backindex')) # 跳转到后端的主页


##############################################################################################################################################################################################################################################


@app.route('/', methods = ['GET', 'POST']) # 前端根目录：产品与团队的介绍页面
def aboutus():
    if g.user is not None and g.user.is_authenticated: # 如已登录，跳至主页
        return redirect(url_for('index'))
    return render_template("/xvlvtao/index.html")


# Providers Page #
@app.route('/index', methods = ['GET', 'POST']) # 前端主页，Home
@login_required # 需要登录方能访问
def index():
    user = g.user
    if user.level == 1:
        return render_template('xvlvtao/index1.html', user = user, groups = user.groups.all())
    else: # user.level == 2
        form = SearchForm()
        if form.validate_on_submit(): # searching
            search_str = '%' + form.search_str.data + '%'
            image_medias_1 = Issue.query.filter(Issue.owner.has(User.id==g.user.id)).filter(Issue.mtype.in_(IMAGES)).filter(Issue.name.like(search_str)).all()
            audio_medias_1 = Issue.query.filter(Issue.owner.has(User.id==g.user.id)).filter(Issue.mtype.in_(AUDIOS)).filter(Issue.name.like(search_str)).all()
            video_medias_1 = Issue.query.filter(Issue.owner.has(User.id==g.user.id)).filter(Issue.mtype.in_(VIDEOS)).filter(Issue.name.like(search_str)).all()
        else: # is not searching # 方法has()用于一对多关系，方法any()用于多对多关系
            image_medias_1 = Issue.query.filter(Issue.owner.has(User.id==g.user.id)).filter(Issue.mtype.in_(IMAGES)).all()
            audio_medias_1 = Issue.query.filter(Issue.owner.has(User.id==g.user.id)).filter(Issue.mtype.in_(AUDIOS)).all()
            video_medias_1 = Issue.query.filter(Issue.owner.has(User.id==g.user.id)).filter(Issue.mtype.in_(VIDEOS)).all()
        medias_1 = [image_medias_1, audio_medias_1, video_medias_1]
        if form.search_str.data:
            placeholder = form.search_str.data
        else:
            placeholder = 'Search...'
        return render_template('xvlvtao/provider.html', user = user, groups = user.groups.all(), form = form, placeholder = placeholder, medias1 = medias_1)


# Private Upload Page #
@app.route('/private', methods = ['GET', 'POST'])
@login_required
def private():
    form = SearchForm()
    user = g.user
    if form.validate_on_submit(): # searching
        search_str = '%' + form.search_str.data + '%'
        image_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(IMAGES)).filter(Media.name.like(search_str)).all()
        audio_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(AUDIOS)).filter(Media.name.like(search_str)).all()
        video_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(VIDEOS)).filter(Media.name.like(search_str)).all()
    else: # is not searching # 方法has()用于一对多关系，方法any()用于多对多关系
        image_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(IMAGES)).all()
        audio_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(AUDIOS)).all()
        video_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(VIDEOS)).all()
    medias_1 = [image_medias_1, audio_medias_1, video_medias_1]
    if form.search_str.data:
        placeholder = form.search_str.data
    else:
        placeholder = 'Search...'
    return render_template("xvlvtao/private-upload.html", title = 'Home',
        form = form, placeholder = placeholder,
        user = user,
        groups = user.groups.all(),
        medias1 = medias_1)


@app.route('/private-download', methods = ['GET', 'POST'])
@login_required
def private_download():
    form = SearchForm()
    user = g.user
    if form.validate_on_submit(): # searching
        search_str = '%' + form.search_str.data + '%'
        image_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(IMAGES)).filter(Media.name.like(search_str)).all()
        audio_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(AUDIOS)).filter(Media.name.like(search_str)).all()
        video_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(VIDEOS)).filter(Media.name.like(search_str)).all()
        image_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(IMAGES)).filter(Issue.name.like(search_str)).all()
        audio_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(AUDIOS)).filter(Issue.name.like(search_str)).all()
        video_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(VIDEOS)).filter(Issue.name.like(search_str)).all()
    else: # is not searching # 方法has()用于一对多关系，方法any()用于多对多关系
        image_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(IMAGES)).all()
        audio_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(AUDIOS)).all()
        video_medias_1 = Media.query.filter(Media.owner.has(User.id==g.user.id)).filter(Media.mtype.in_(VIDEOS)).all()
        image_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(IMAGES)).all()
        audio_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(AUDIOS)).all()
        video_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(VIDEOS)).all()
    medias_1 = [image_medias_1 + image_issues_1, audio_medias_1 + audio_issues_1, video_medias_1 + video_issues_1]
    if form.search_str.data:
        placeholder = form.search_str.data
    else:
        placeholder = 'Search...'
    return render_template("xvlvtao/download.html", title = 'Home',
        form = form, placeholder = placeholder,
        user = user,
        groups = user.groups.all(),
        medias1 = medias_1)


@app.route('/private-buy', methods = ['GET', 'POST'])
@login_required
def private_buy():
    form = SearchForm()
    user = g.user
    if form.validate_on_submit(): # searching
        search_str = '%' + form.search_str.data + '%'
        image_medias_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(IMAGES)).filter(Issue.name.like(search_str)).all()
        audio_medias_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(AUDIOS)).filter(Issue.name.like(search_str)).all()
        video_medias_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(VIDEOS)).filter(Issue.name.like(search_str)).all()
    else: # is not searching # 方法has()用于一对多关系，方法any()用于多对多关系
        image_medias_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(IMAGES)).all()
        audio_medias_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(AUDIOS)).all()
        video_medias_1 = Issue.query.filter(Issue.whosbuy.any(User.id==g.user.id)).filter(Issue.mtype.in_(VIDEOS)).all()
    medias_1 = [image_medias_1, audio_medias_1, video_medias_1]
    if form.search_str.data:
        placeholder = form.search_str.data
    else:
        placeholder = 'Search...'
    return render_template("xvlvtao/buy.html", title = 'Home',
        form = form, placeholder = placeholder,
        user = user,
        groups = user.groups.all(),
        medias1 = medias_1)


@app.route('/private-collect', methods = ['GET', 'POST'])
@login_required
def private_collect():
    form = SearchForm()
    user = g.user
    if form.validate_on_submit(): # searching
        search_str = '%' + form.search_str.data + '%'
        image_medias_1 = Media.query.filter(Media.favors.any(User.id==g.user.id)).filter(Media.mtype.in_(IMAGES)).filter(Media.name.like(search_str)).all()
        image_issues_1 = Issue.query.filter(Issue.ifavors.any(User.id==g.user.id)).filter(Issue.mtype.in_(IMAGES)).filter(Media.name.like(search_str)).all()
        audio_medias_1 = Media.query.filter(Media.favors.any(User.id==g.user.id)).filter(Media.mtype.in_(AUDIOS)).filter(Media.name.like(search_str)).all()
        audio_issues_1 = Issue.query.filter(Issue.ifavors.any(User.id==g.user.id)).filter(Issue.mtype.in_(AUDIOS)).filter(Media.name.like(search_str)).all()
        video_medias_1 = Media.query.filter(Media.favors.any(User.id==g.user.id)).filter(Media.mtype.in_(VIDEOS)).filter(Media.name.like(search_str)).all()
        video_issues_1 = Issue.query.filter(Issue.ifavors.any(User.id==g.user.id)).filter(Issue.mtype.in_(VIDEOS)).filter(Media.name.like(search_str)).all()
    else: # is not searching # 方法has()用于一对多关系，方法any()用于多对多关系
        image_medias_1 = Media.query.filter(Media.favors.any(User.id==g.user.id)).filter(Media.mtype.in_(IMAGES)).all()
        image_issues_1 = Issue.query.filter(Issue.ifavors.any(User.id==g.user.id)).filter(Issue.mtype.in_(IMAGES)).all()
        audio_medias_1 = Media.query.filter(Media.favors.any(User.id==g.user.id)).filter(Media.mtype.in_(AUDIOS)).all()
        audio_issues_1 = Issue.query.filter(Issue.ifavors.any(User.id==g.user.id)).filter(Issue.mtype.in_(AUDIOS)).all()
        video_medias_1 = Media.query.filter(Media.favors.any(User.id==g.user.id)).filter(Media.mtype.in_(VIDEOS)).all()
        video_issues_1 = Issue.query.filter(Issue.ifavors.any(User.id==g.user.id)).filter(Issue.mtype.in_(VIDEOS)).all()
    medias_1 = [image_medias_1 + image_issues_1, audio_medias_1 + audio_issues_1, video_medias_1 + video_issues_1]
    if form.search_str.data:
        placeholder = form.search_str.data
    else:
        placeholder = 'Search...'
    return render_template("xvlvtao/collects.html", title = 'Home',
        form = form, placeholder = placeholder,
        user = user,
        groups = user.groups.all(),
        medias1 = medias_1)


@app.route('/group/<int:gid>', methods = ['GET', 'POST'])
@login_required
def group(gid):
    form = SearchForm()
    user = g.user
    users = User.query.filter(User.groups.any(Group.id == gid)).filter(User.id != user.id).all()
    if form.validate_on_submit(): # searching
        search_str = '%' + form.search_str.data + '%'
        image_medias_1 = Media.query.filter(Media.owner.has(User.id.in_(map(item2id, users)))).filter(Media.privilege==2).filter(Media.mtype.in_(IMAGES)).filter(Media.name.like(search_str)).all()
        audio_medias_1 = Media.query.filter(Media.owner.has(User.id.in_(map(item2id, users)))).filter(Media.privilege==2).filter(Media.mtype.in_(AUDIOS)).filter(Media.name.like(search_str)).all()
        video_medias_1 = Media.query.filter(Media.owner.has(User.id.in_(map(item2id, users)))).filter(Media.privilege==2).filter(Media.mtype.in_(VIDEOS)).filter(Media.name.like(search_str)).all()
        image_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id.in_(map(item2id, users)))).filter(Issue.buyers.any(Association.extra_privilege==2)).filter(Issue.mtype.in_(IMAGES)).filter(Issue.name.like(search_str)).all()
        audio_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id.in_(map(item2id, users)))).filter(Issue.buyers.any(Association.extra_privilege==2)).filter(Issue.mtype.in_(AUDIOS)).filter(Issue.name.like(search_str)).all()
        video_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id.in_(map(item2id, users)))).filter(Issue.buyers.any(Association.extra_privilege==2)).filter(Issue.mtype.in_(VIDEOS)).filter(Issue.name.like(search_str)).all()
    else: # is not searching # 方法has()用于一对多关系，方法any()用于多对多关系
        image_medias_1 = Media.query.filter(Media.owner.has(User.id.in_(map(item2id, users)))).filter(Media.privilege==2).filter(Media.mtype.in_(IMAGES)).all()
        audio_medias_1 = Media.query.filter(Media.owner.has(User.id.in_(map(item2id, users)))).filter(Media.privilege==2).filter(Media.mtype.in_(AUDIOS)).all()
        video_medias_1 = Media.query.filter(Media.owner.has(User.id.in_(map(item2id, users)))).filter(Media.privilege==2).filter(Media.mtype.in_(VIDEOS)).all()
        image_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id.in_(map(item2id, users)))).filter(Issue.buyers.any(Association.extra_privilege==2)).filter(Issue.mtype.in_(IMAGES)).all()
        audio_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id.in_(map(item2id, users)))).filter(Issue.buyers.any(Association.extra_privilege==2)).filter(Issue.mtype.in_(AUDIOS)).all()
        video_issues_1 = Issue.query.filter(Issue.whosbuy.any(User.id.in_(map(item2id, users)))).filter(Issue.buyers.any(Association.extra_privilege==2)).filter(Issue.mtype.in_(VIDEOS)).all()
    medias_1 = [image_medias_1 + image_issues_1, audio_medias_1 + audio_issues_1, video_medias_1 + video_issues_1]
    if form.search_str.data:
        placeholder = form.search_str.data
    else:
        placeholder = 'Search...'
    return render_template("xvlvtao/group.html", title = 'Home',
        form = form, placeholder = placeholder,
        user = user,
        groups = user.groups.all(),
        medias1 = medias_1)


# Publishs Page #
@app.route('/publish', methods = ['GET', 'POST'])
@login_required
def publish():
    form = SearchForm()
    user = g.user
    if form.validate_on_submit(): # searching
        search_str = '%' + form.search_str.data + '%'
        image_medias_1 = Issue.query.filter(Issue.mtype.in_(IMAGES)).filter(Issue.name.like(search_str)).all()
        audio_medias_1 = Issue.query.filter(Issue.mtype.in_(AUDIOS)).filter(Issue.name.like(search_str)).all()
        video_medias_1 = Issue.query.filter(Issue.mtype.in_(VIDEOS)).filter(Issue.name.like(search_str)).all()
    else: # is not searching # 方法has()用于一对多关系，方法any()用于多对多关系
        image_medias_1 = Issue.query.filter(Issue.mtype.in_(IMAGES)).all()
        audio_medias_1 = Issue.query.filter(Issue.mtype.in_(AUDIOS)).all()
        video_medias_1 = Issue.query.filter(Issue.mtype.in_(VIDEOS)).all()
    medias_1 = [image_medias_1, audio_medias_1, video_medias_1]
    if form.search_str.data:
        placeholder = form.search_str.data
    else:
        placeholder = 'Search...'
    return render_template("xvlvtao/publish.html", title = 'Home',
        form = form, placeholder = placeholder,
        user = user,
        groups = user.groups.all(),
        medias1 = medias_1)


# Media Player
@app.route('/single/<int:mid>/<int:model>', methods = ['GET', 'POST'])
@login_required
def single(mid, model):
    m = Media.query.filter(Media.id == mid).first()
    if m:
        m.viewers += 1
        db.session.add(m)
        db.session.commit() # one more views
        m = Media.query.filter(Media.id == mid).first()
        t = m.timestamp.strftime('%A %Y-%m-%d %H:%M:%S')
    else:
        t = ""
    UpNext = Media.query.filter(Media.owner.has(User.id==g.user.id)).all()[:7]
    return render_template("xvlvtao/single.html", mid=mid, m=m, t=t, user=g.user, groups = g.user.groups.all(), UpNext = UpNext, model = model)
@app.route('/player/<mid>/<int:model>', methods = ['GET', 'POST'])
@login_required
def player(mid, model):
    m = Media.query.filter(Media.id == mid).first()
    if m.mtype == 'mp3':
        return render_template("xvlvtao/musicplayer.html", m=m, user=g.user, model = model)
    elif m.mtype == 'mp4':
        return render_template("xvlvtao/videoplayer.html", m=m, user=g.user, model = model)
    else:
        return render_template("xvlvtao/photobox.html", m=m, user=g.user, model = model)

# Issue Player
@app.route('/isingle/<mid>/<int:model>', methods = ['GET', 'POST'])
@login_required
def isingle(mid, model):
    m = Issue.query.filter(Issue.id == mid).first()
    if m:
        m.viewers += 1
        db.session.add(m)
        db.session.commit() # one more views
        m = Issue.query.filter(Issue.id == mid).first()
        t = m.timestamp.strftime('%A %Y-%m-%d %H:%M:%S')
    else:
        t = ""
    UpNext = Issue.query.filter(Issue.owner.has(User.id==m.owner.id)).all()[:7]
    return render_template("xvlvtao/single.html", mid=mid, m=m, t=t, user=g.user, groups = g.user.groups.all(), UpNext = UpNext, model = model)
@app.route('/iplayer/<mid>/<int:model>', methods = ['GET', 'POST'])
@login_required
def iplayer(mid, model):
    m = Issue.query.filter(Issue.id == mid).first()
    print(m)
    if m.mtype == 'mp3':
        return render_template("xvlvtao/musicplayer.html", m=m, user=g.user, model = model)
    elif m.mtype == 'mp4':
        return render_template("xvlvtao/videoplayer.html", m=m, user=g.user, model = model)
    else:
        return render_template("xvlvtao/photobox.html", m=m, user=g.user, model = model)