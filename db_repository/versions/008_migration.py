from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
media = Table('media', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
    Column('head', VARCHAR(length=40)),
)

media = Table('media', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('furl', String(length=200)),
    Column('mtype', String(length=40)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['media'].columns['body'].drop()
    pre_meta.tables['media'].columns['head'].drop()
    post_meta.tables['media'].columns['furl'].create()
    post_meta.tables['media'].columns['mtype'].create()
    post_meta.tables['media'].columns['name'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['media'].columns['body'].create()
    pre_meta.tables['media'].columns['head'].create()
    post_meta.tables['media'].columns['furl'].drop()
    post_meta.tables['media'].columns['mtype'].drop()
    post_meta.tables['media'].columns['name'].drop()
