import sys
from app import db, models
if sys.argv[1] == 1:
	families = models.Family.query.all()
	for f in families:
		db.session.delete()
if sys.argv[1] == 2:
	passusers = models.User.query.all()
	for u in users:
    	db.session.delete(u)
if sys.argv[1] == 3:
	medias = models.Media.query.all()
	for m in medias:
    	db.session.delete(m)
db.session.commit()