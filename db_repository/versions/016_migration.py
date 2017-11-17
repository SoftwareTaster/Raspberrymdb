from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tags = Table('tags', pre_meta,
    Column('user_id', INTEGER),
    Column('group_id', INTEGER),
)

ins = Table('ins', post_meta,
    Column('user_id', Integer),
    Column('group_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tags'].drop()
    post_meta.tables['ins'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['tags'].create()
    post_meta.tables['ins'].drop()
