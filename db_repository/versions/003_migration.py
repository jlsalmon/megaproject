from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
task = Table('task', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=256)),
    Column('start_date', Date),
    Column('end_date', Date),
    Column('info', String(length=256)),
    Column('project_id', Integer),
    Column('owner_id', Integer),
    Column('parent_task', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['task'].columns['info'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['task'].columns['info'].drop()
