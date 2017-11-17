#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, session, redirect, url_for, escape, request
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from flask import Flask, request, render_template
# from flask.ext.restful import Resource, Api

# conn = sqlite3.connect('test.db') # 连接到SQLite数据库，数据库文件是test.db，如果文件不存在，会自动在当前目录创建
# cursor = conn.cursor() # 创建一个Cursor
# cursor.execute('create table user (id varchar(20) primary key, name varchar(20))') # 执行一条SQL语句，创建user表
# cursor.close() # 关闭Cursor
# conn.commit() # 提交事务
# conn.close() # 关闭Connection

# 创建对象的基类:
Base = declarative_base()
# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'
    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    password = Column(String(20))
# 初始化数据库连接:
engine = create_engine('sqlite:///foo.db')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# api = Api(app)
# todos = {}
# class TodoSimple(Resource):
#     def get(self, todo_id):
#         return {todo_id: todos[todo_id]}
#     def put(self, todo_id):
#         todos[todo_id] = request.form['data']
#         return {todo_id: todos[todo_id]}
# api.add_resource(TodoSimple, '/<string:todo_id>')

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.run(debug=True)