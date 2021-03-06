"""Initial migration.

Revision ID: 2608ca0d0b58
Revises: 
Create Date: 2022-02-05 22:33:48.654369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2608ca0d0b58'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('_password', sa.LargeBinary(length=120), nullable=True),
    sa.Column('_salt', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('author',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('isbn', sa.Integer(), nullable=False),
    sa.Column('fio', sa.String(length=80), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn')
    )
    op.create_table('book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('isbn', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('number_of_pages', sa.Integer(), nullable=False),
    sa.Column('review', sa.Text(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book')
    op.drop_table('author')
    op.drop_table('user')
    # ### end Alembic commands ###
