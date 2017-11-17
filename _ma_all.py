# encoding: utf-8
import sys
from app import db, models
savedStdout = sys.stdout # 保存标准输出流
with open('_ma.txt', 'w+') as file:
	sys.stdout = file # 标准输出重定向至文件
	families = models.Family.query.all()
	print families
	for f in families:
		users = f.users.all()
		print '\t', users
	users = models.User.query.all()
	print users
	for u in users:
		print u.id,u.nickname,u.email
		medias = u.medias.all()
		print '\t', medias
		for m in medias:
			print '\t',m.owner.nickname,unicode(m.name).encode('utf-8'),m.furl,m.mtype,m.timestamp
sys.stdout = savedStdout # 恢复标准输出流