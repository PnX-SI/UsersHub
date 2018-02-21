#!/bin/bash

. config/settings.ini

echo "Créer les fichiers de configurations en lien avec la base de données..."
cp config/connecter.php.sample config/connecter.php
cp config/dbconnexions.json.sample config/dbconnexions.json
cp -n config/config.php.sample config/config.php
cp -n web/js/settings.js.sample web/js/settings.js
cp -n web/images/main_logo.png.sample web/images/main_logo.png
cp -n web/images/bandeau_utilisateurs.png.sample web/images/bandeau_utilisateurs.png


echo "Configuration du fichier config/connecter.php..."
sed -i "s/serveur='.*$/serveur='$db_host';/" config/connecter.php
sed -i "s/user='.*$/user='$user_pg';/" config/connecter.php
sed -i "s/passe='.*$/passe='$user_pg_pass';/" config/connecter.php
sed -i "s/base='.*$/base='$db_name';/" config/connecter.php
sed -i "s/port='.*$/port='$pg_port';/" config/connecter.php

echo "Configuration initiale du fichier config/dbconnexions.json"
rm config/dbconnexions.json
touch config/dbconnexions.json
echo "{" >> config/dbconnexions.json
echo "    \"databases\":" >> config/dbconnexions.json
echo "    [" >> config/dbconnexions.json
echo "        {" >> config/dbconnexions.json  
echo "            \"dbfunname\":\"Utilisateurs\"" >> config/dbconnexions.json 
echo "            ,\"host\":\"$db_host\"" >> config/dbconnexions.json 
echo "            ,\"dbname\":\"$db_name\"" >> config/dbconnexions.json 
echo "            ,\"user\":\"$user_pg\"" >> config/dbconnexions.json 
echo "            ,\"pass\":\"$user_pg_pass\"" >> config/dbconnexions.json 
echo "            ,\"port\":\"$pg_port\"" >> config/dbconnexions.json 
echo "        }" >> config/dbconnexions.json
echo "    ]" >> config/dbconnexions.json
echo "}" >> config/dbconnexions.json


APACHE_REP=/var/www/
if /usr/sbin/apache2 -v | grep -q version.*2.4; then
    echo apache 2.4
	APACHE_REP=/var/www/html
fi

echo "Fin. Vous devez manuellement éditer le fichier config/dbconnexoins.json et y ajouter les paramètres de connexions à toutes les bases que vous souhaitez synchroniser avec UsersHub"
