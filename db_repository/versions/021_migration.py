from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
buy_media = Table('buy_media', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('furl', String(length=200)),
    Column('mtype', String(length=40)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

collect_media = Table('collect_media', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('furl', String(length=200)),
    Column('mtype', String(length=40)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
    Column('level', Integer),
    Column('about_me', String(length=140)),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['buy_media'].create()
    post_meta.tables['collect_media'].create()
    post_meta.tables['user'].columns['level'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['buy_media'].drop()
    post_meta.tables['collect_media'].drop()
    post_meta.tables['user'].columns['level'].drop()
