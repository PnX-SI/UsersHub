#!/bin/bash

. config/settings.ini

# Création des fichiers de configuration
cd config

echo "Création du fichier de configuration ..."
if [ ! -f config.py ]; then
  cp config.py.sample config.py
fi

echo "préparation du fichier config.py..."
sed -i "s/SQLALCHEMY_DATABASE_URI = .*$/SQLALCHEMY_DATABASE_URI = \"postgresql:\/\/$user_pg:$user_pg_pass@$db_host:$pg_port\/$db_name\"/" config.py

url_application="${url_application//\//\\/}"
# on enleve le / final
if [ "${url_application: -1}" = '/' ]
then
url_application="${url_application::-1}"
fi
sed -i "s/URL_APPLICATION =.*$/URL_APPLICATION ='$url_application'/g" config.py

cd ..

# Installation de l'environement python

echo "Installation du virtual env..."
python -m virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# rendre la commande nvm disponible
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
# Installation de l'environement javascript
cd app/static
nvm install 
nvm use
npm ci
cd ../..


#Lancement de l'application
DIR=$(readlink -e "${0%/*}")
currentdir=${PWD##*/} 


sudo -s cp usershub-service.conf /etc/supervisor/conf.d/
sudo -s sed -i "s%APP_PATH%${DIR}%" /etc/supervisor/conf.d/usershub-service.conf

# activate proxy apache extension
sudo a2enmod proxy
sudo a2enmod proxy_http

# lancement des services qui créent les fichiers de logs
sudo -s supervisorctl reread
sudo -s supervisorctl reload

#création d'un fichier rotation des logs une fois qu'ils sont créés
sudo cp $DIR/log_rotate /etc/logrotate.d/uhv2
sudo -s sed -i "s%APP_PATH%${DIR}%" /etc/logrotate.d/uhv2
sudo logrotate -f /etc/logrotate.conf