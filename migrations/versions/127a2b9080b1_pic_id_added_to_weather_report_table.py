"""pic id added to weather report table

Revision ID: 127a2b9080b1
Revises: f4a49fd05e68
Create Date: 2020-09-30 01:27:42.597890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '127a2b9080b1'
down_revision = 'f4a49fd05e68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('good_morning_report', sa.Column('pic_id', sa.String(length=10), nullable=True))
    op.execute("UPDATE good_morning_report SET pic_id = '10d'")
    op.alter_column('good_morning_report', 'pic_id', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('good_morning_report', 'pic_id')
    # ### end Alembic commands ###
