"""UsersHub

Revision ID: 9445a69f2bed
Revises: fa35dfe5ff27
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
    '72f227e37bdf',  # schema utilisateurs, données d’exemples
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
        (6, (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'UH')),
        (3, (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'UH'))
    """)
    op.execute("""
    INSERT INTO cor_role_app_profil (id_role, id_application, id_profil) VALUES
    (
        (SELECT id_role FROM t_roles WHERE nom_role = 'Grp_admin'),
        (SELECT id_application FROM t_applications WHERE code_application = 'UH'),
        (SELECT id_profil FROM t_profils WHERE code_profil = '6')
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
