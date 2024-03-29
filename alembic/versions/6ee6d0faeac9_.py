"""empty message

Revision ID: 6ee6d0faeac9
Revises: 80247c0fdece
Create Date: 2022-11-05 00:29:48.337660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ee6d0faeac9'
down_revision = '80247c0fdece'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('playlists_owner_id_fkey', 'playlists', type_='foreignkey')
    op.create_foreign_key(None, 'playlists', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('tracks_in_playlists_playlist_id_fkey', 'tracks_in_playlists', type_='foreignkey')
    op.create_foreign_key(None, 'tracks_in_playlists', 'playlists', ['playlist_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tracks_in_playlists', type_='foreignkey')
    op.create_foreign_key('tracks_in_playlists_playlist_id_fkey', 'tracks_in_playlists', 'playlists', ['playlist_id'], ['id'])
    op.drop_constraint(None, 'playlists', type_='foreignkey')
    op.create_foreign_key('playlists_owner_id_fkey', 'playlists', 'users', ['owner_id'], ['id'])
    # ### end Alembic commands ###
