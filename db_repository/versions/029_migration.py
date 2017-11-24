from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
media = Table('media', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('curl', String(length=200)),
    Column('furl', String(length=200)),
    Column('mtype', String(length=40)),
    Column('privilege', Integer),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('viewers', Integer),
)

issue = Table('issue', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('wurl', String(length=200)),
    Column('furl', String(length=200)),
    Column('mtype', String(length=40)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
    Column('viewers', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['media'].columns['viewers'].create()
    post_meta.tables['issue'].columns['viewers'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['media'].columns['viewers'].drop()
    post_meta.tables['issue'].columns['viewers'].drop()
