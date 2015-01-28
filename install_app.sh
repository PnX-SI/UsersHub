#!/bin/bash

. config/settings.ini

echo "configuration du fichier config/connecter.php..."
sed -i "s/$user='.*$/$user='$user_pg';/" config/connecter.php
sed -i "s/$passe='.*$/$passe='$user_pg_pass';/" config/connecter.php
sed -i "s/$base='.*$/$base='$db_name';/" config/connecter.php

echo "Suppression des fichiers de log de l'installation..."
rm log/*.log


echo "Configuration du répertoire web de l'application..."
sudo ln -s ${PWD}/ /var/www/usershub
echo "Fin. Vous devez manuellement éditer le fichier dbconnexoins.json et y ajouter les paramètres de connexions à toutes les bases que vous souhaitez synchroniser avec UsersHub"
