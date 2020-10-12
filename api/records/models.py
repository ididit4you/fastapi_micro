import sqlalchemy as sa

metadata = sa.MetaData()

record = sa.Table(
    'record',
    metadata,
    sa.Column('id', sa.Integer(), primary_key=True),
    sa.Column('text', sa.String(), nullable=False),
)
