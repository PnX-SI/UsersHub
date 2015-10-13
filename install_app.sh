#!/bin/bash

. config/settings.ini

echo "Créer les fichiers de configurations en lien avec la base de données..."
cp config/connecter.php.sample config/connecter.php
cp config/dbconnexions.json.sample config/dbconnexions.json
cp -n web/js/settings.js.sample web/js/settings.js.sample
cp -n web/images/main_logo.png.sample web/images/main_logo.png
cp -n web/images/bandeau_utilisateurs.png.sample web/images/bandeau_utilisateurs.png


echo "Configuration du fichier config/connecter.php..."
sed -i "s/user='.*$/user='$user_pg';/" config/connecter.php
sed -i "s/passe='.*$/passe='$user_pg_pass';/" config/connecter.php
sed -i "s/base='.*$/base='$db_name';/" config/connecter.php

echo "Suppression des fichiers de log de l'installation..."
sudo rm log/*.log


APACHE_REP=/var/www/
if /usr/sbin/apache2 -v | grep -q version.*2.4; then
    echo apache 2.4
	APACHE_REP=/var/www/html
fi


if [ ! -h $APACHE_REP/usershub ]; then
  echo "Configuration du répertoire web de l'application..."
  cd web
  sudo ln -s ${PWD}/ $APACHE_REP/usershub
  cd ..
else
  echo "Le répertoire de l'application exite déjà"
fi
echo "Fin. Vous devez manuellement éditer le fichier config/dbconnexoins.json et y ajouter les paramètres de connexions à toutes les bases que vous souhaitez synchroniser avec UsersHub"
