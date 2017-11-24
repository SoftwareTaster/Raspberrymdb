from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
purchase = Table('purchase', pre_meta,
    Column('user_id', INTEGER),
    Column('issue_id', INTEGER),
)

purchase = Table('purchase', post_meta,
    Column('user_id', Integer),
    Column('media_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['purchase'].columns['issue_id'].drop()
    post_meta.tables['purchase'].columns['media_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['purchase'].columns['issue_id'].create()
    post_meta.tables['purchase'].columns['media_id'].drop()
