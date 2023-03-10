"""empty message

Revision ID: 2964e361c130
Revises: 
Create Date: 2023-02-06 15:55:30.863628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2964e361c130'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sections_id'), 'sections', ['id'], unique=False)
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['sections.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    op.alter_column('athletes', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('athletes', 'license',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('athletes', 'birthday',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('athletes', 'category',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.add_column('marks', sa.Column('date', sa.Date(), nullable=True))
    op.add_column('marks', sa.Column('event', sa.String(), nullable=True))
    op.add_column('marks', sa.Column('athlete_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'marks', 'athletes', ['athlete_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'marks', type_='foreignkey')
    op.drop_column('marks', 'athlete_id')
    op.drop_column('marks', 'event')
    op.drop_column('marks', 'date')
    op.alter_column('athletes', 'category',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('athletes', 'birthday',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('athletes', 'license',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('athletes', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_sections_id'), table_name='sections')
    op.drop_table('sections')
    # ### end Alembic commands ###
