"""empty message

Revision ID: 2baa0360ca8b
Revises: 007472cc24bc
Create Date: 2023-01-13 08:21:12.877918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2baa0360ca8b'
down_revision = '007472cc24bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('address', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
