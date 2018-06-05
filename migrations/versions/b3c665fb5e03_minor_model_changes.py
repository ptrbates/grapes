"""minor model changes

Revision ID: b3c665fb5e03
Revises: 939cfa87558e
Create Date: 2018-06-02 13:36:38.373612

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3c665fb5e03'
down_revision = '939cfa87558e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('multiplier_list')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('multiplier_list',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('grades_ML', sa.FLOAT(), nullable=True),
    sa.Column('weeks_year', sa.INTEGER(), nullable=True),
    sa.Column('ft_exp', sa.INTEGER(), nullable=True),
    sa.Column('recess', sa.FLOAT(), nullable=True),
    sa.Column('arts_movement', sa.FLOAT(), nullable=True),
    sa.Column('fl', sa.FLOAT(), nullable=True),
    sa.Column('stem', sa.FLOAT(), nullable=True),
    sa.Column('hum_chem', sa.FLOAT(), nullable=True),
    sa.Column('grades_spec', sa.FLOAT(), nullable=True),
    sa.Column('other', sa.FLOAT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
