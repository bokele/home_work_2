"""empty message

Revision ID: 362fff5c9015
Revises: 
Create Date: 2020-11-16 21:52:29.491570

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '362fff5c9015'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('todo_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_name', sa.String(length=80), nullable=False),
    sa.Column('task_body', sa.Text(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('todo_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['todo_id'], ['todo_lists.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_lists')
    op.drop_table('todo_lists')
    # ### end Alembic commands ###
