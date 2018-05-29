"""added MultiplierList schema

Revision ID: 939cfa87558e
Revises: 48f326ca4fde
Create Date: 2018-05-27 15:59:16.194606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '939cfa87558e'
down_revision = '48f326ca4fde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('multiplier_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grades_ML', sa.Float(), nullable=True),
    sa.Column('weeks_year', sa.Integer(), nullable=True),
    sa.Column('ft_exp', sa.Integer(), nullable=True),
    sa.Column('recess', sa.Float(), nullable=True),
    sa.Column('arts_movement', sa.Float(), nullable=True),
    sa.Column('fl', sa.Float(), nullable=True),
    sa.Column('stem', sa.Float(), nullable=True),
    sa.Column('hum_chem', sa.Float(), nullable=True),
    sa.Column('grades_spec', sa.Float(), nullable=True),
    sa.Column('other', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('multiplier_list')
    # ### end Alembic commands ###