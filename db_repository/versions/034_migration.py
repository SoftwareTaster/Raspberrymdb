from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
buy = Table('buy', pre_meta,
    Column('user_id', INTEGER, primary_key=True, nullable=False),
    Column('issue_id', INTEGER, primary_key=True, nullable=False),
    Column('extra_privilege', INTEGER),
)

purchase = Table('purchase', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('issue_id', Integer, primary_key=True, nullable=False),
    Column('extra_privilege', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['buy'].drop()
    post_meta.tables['purchase'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['buy'].create()
    post_meta.tables['purchase'].drop()
