from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
buy_media = Table('buy_media', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=100)),
    Column('furl', VARCHAR(length=200)),
    Column('mtype', VARCHAR(length=40)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

collect_media = Table('collect_media', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('furl', VARCHAR(length=200)),
    Column('mtype', VARCHAR(length=40)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

havethe = Table('havethe', pre_meta,
    Column('user_id', INTEGER),
    Column('media_id', INTEGER),
)

favorite = Table('favorite', post_meta,
    Column('user_id', Integer),
    Column('media_id', Integer),
)

issue = Table('issue', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('furl', String(length=200)),
    Column('mtype', String(length=40)),
    Column('timestamp', DateTime),
)

purchase = Table('purchase', post_meta,
    Column('user_id', Integer),
    Column('issue_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['buy_media'].drop()
    pre_meta.tables['collect_media'].drop()
    pre_meta.tables['havethe'].drop()
    post_meta.tables['favorite'].create()
    post_meta.tables['issue'].create()
    post_meta.tables['purchase'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['buy_media'].create()
    pre_meta.tables['collect_media'].create()
    pre_meta.tables['havethe'].create()
    post_meta.tables['favorite'].drop()
    post_meta.tables['issue'].drop()
    post_meta.tables['purchase'].drop()
