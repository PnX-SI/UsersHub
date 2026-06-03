#!/usr/bin/env bash

. config/settings.ini || exit 1

# Tell GeoNature where to find UsersHub alembic revision files
grep '\[ALEMBIC\]' "/home/${USER}/geonature/config/geonature_config.toml" > /dev/null || echo -e "\n[ALEMBIC]\nVERSION_LOCATIONS = '/home/${USER}/usershub/app/migrations/versions/'" >> "/home/${USER}/geonature/config/geonature_config.toml"

source "/home/${USER}/geonature/backend/venv/bin/activate"

geonature db upgrade usershub-samples@head
deactivate

sudo systemctl start $app_name || exit 1

