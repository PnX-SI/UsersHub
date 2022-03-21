#!/bin/bash

. config/settings.ini || exit 1

# Création des fichiers de configuration
cd config


echo "Création du fichier de configuration ..."
if [ ! -f config.py ]; then
  cp config.py.sample config.py || exit 1

  echo "préparation du fichier config.py..."
  sed -i "s/SQLALCHEMY_DATABASE_URI = .*$/SQLALCHEMY_DATABASE_URI = \"postgresql:\/\/$user_pg:$user_pg_pass@$db_host:$pg_port\/$db_name\"/" config.py || exit 1
  
  url_application="${url_application//\//\\/}"
  # on enleve le / final
  if [ "${url_application: -1}" = '/' ]
  then
  url_application="${url_application::-1}"
  fi
  sed -i "s/URL_APPLICATION =.*$/URL_APPLICATION ='$url_application'/g" config.py || exit 1
fi

cd ..

# Installation de l'environement python

echo "Installation du virtual env..."
python3 -m venv venv || exit 1
source venv/bin/activate
pip install --upgrade pip || exit 1
if [ "${mode}" = "dev" ]; then
    pip install -r requirements-dev.txt || exit 1
else
    pip install -r requirements.txt || exit 1
fi

deactivate

# rendre la commande nvm disponible
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
# Installation de l'environement javascript
cd app/static
nvm install || exit 1
nvm use || exit 1
npm ci || exit 1
cd ../..


#Lancement de l'application
export USERSHUB_DIR=$(readlink -e "${0%/*}")

# Configuration systemd
envsubst '${USER} ${USERSHUB_DIR}' < usershub.service | sudo tee /etc/systemd/system/usershub.service || exit 1
sudo systemctl daemon-reload || exit 1

# Configuration apache
sudo cp usershub_apache.conf /etc/apache2/conf-available/usershub.conf || exit 1
sudo a2enmod proxy || exit 1
sudo a2enmod proxy_http || exit 1
# you may need a restart if proxy & proxy_http was not already enabled

echo "Vous pouvez maintenant démarrer UsersHub avec la commande : sudo systemctl start usershub"
