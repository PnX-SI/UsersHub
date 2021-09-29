"""UsersHub

Revision ID: 9445a69f2bed
Create Date: 2021-08-30 16:33:42.410504

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9445a69f2bed'
down_revision = None
branch_labels = ('usershub',)
depends_on = (
    'fa35dfe5ff27',  # schema utilisateurs
)


def upgrade():
    op.execute("""
    INSERT INTO utilisateurs.t_applications (
        code_application,
        nom_application,
        desc_application,
        id_parent)
    VALUES (
        'UH',
        'UsersHub',
        'Application permettant d''administrer la présente base de données.',
        NULL)
    """)
    op.execute("""
    INSERT INTO utilisateurs.cor_profil_for_app
        (id_profil, id_application)
    VALUES
        (
            (SELECT id_profil FROM utilisateurs.t_profils WHERE code_profil = '6'),
            (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'UH')
        ), (
            (SELECT id_profil FROM utilisateurs.t_profils WHERE code_profil = '3'),
            (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'UH')
        )
    """)


def downgrade():
    op.execute("""
    DELETE FROM utilisateurs.cor_profil_for_app cor
    USING utilisateurs.t_applications app
    WHERE cor.id_application = app.id_application
    AND app.code_application = 'UH'
    """)
    op.execute("DELETE FROM utilisateurs.t_applications WHERE code_application = 'UH'")
