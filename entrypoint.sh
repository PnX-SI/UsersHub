#!/bin/bash
BASE_DIR=$PWD

# Création des fichiers de configuration
cd config


echo "Création du fichier de configuration ..."
# TODO générer le config.py à partir du .env
cp config.py.docker config.py



echo "préparation du fichier config.py..."
sed -i "s/SQLALCHEMY_DATABASE_URI = .*$/SQLALCHEMY_DATABASE_URI = \"postgresql:\/\/$user_pg:$user_pg_pass@$pg_host:$pg_port\/$db_name\"/" config.py
echo "config.py done"

url_application="${url_application}"

sed -i "s/URL_APPLICATION =.*$/URL_APPLICATION ='$url_application'/g" config.py

cd $BASE_DIR

# rendre la commande nvm disponible
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
# Installation de l'environement javascript
cd app/static
nvm install
nvm use
npm ci
cd $BASE_DIR
DIR=$PWD
currentdir=${PWD##*/}


#Lancement de l'application
export PYTHONPATH=$BASE_DIR:$PYTHONPATH
export FLASK_APP=server
exec gunicorn docker_server:app --pid="${app_name}.pid" -w "${gun_num_workers}"  -b "${gun_host}:${gun_port}"  -n "${app_name}"

