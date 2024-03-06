import setuptools
from pathlib import Path


root_dir = Path(__file__).absolute().parent
with (root_dir / "VERSION").open() as f:
    version = f.read()
with (root_dir / "README.rst").open() as f:
    long_description = f.read()


setuptools.setup(
    name="usershub",
    description="Application web de gestion centralisée des utilisateurs",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    maintainer="Parcs nationaux des Écrins et des Cévennes",
    maintainer_email="geonature@ecrins-parcnational.fr",
    url="https://github.com/PnX-SI/UsersHub",
    version=version,
    packages=setuptools.find_packages(where=".", include=["app*"]),
    install_requires=(
        list(open("requirements-common.in", "r"))
        + list(open("requirements-dependencies.in", "r"))
    ),
    package_data={
        "app": ["templates/*.html", "templates/*.js"],
        "app.migrations": ["alembic.ini", "script.py.mako"],
    },
    entry_points={
        "alembic": [
            "migrations = app.migrations:versions",
        ],
    },
)
