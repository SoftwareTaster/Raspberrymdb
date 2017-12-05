from app import db, models

users = models.User.query.all()
user = users[0]

issue = models.Issue.query.filter(models.Issue.id==11).first()

a = models.Association(extra_privilege=1)
a.buy = issue
a.buyer = user

db.session.add(a)
db.session.commit()

user.buywhats
issue.whosbuy