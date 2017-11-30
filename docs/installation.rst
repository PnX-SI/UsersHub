===========
APPLICATION
===========

Configuration de la base de données PostgreSQL
==============================================

* Créer et mettre à jour le fichier ``config/settings.ini``
 
  ::  
  
    cp config/settings.ini.sample config/settings.ini
    nano config/settings.ini

Renseigner le nom de la base de données, l'utilisateur PostgreSQL et son mot de passe. Il est possible mais non conseillé de laisser les valeurs proposées par défaut. 

ATTENTION : Les valeurs renseignées dans ce fichier sont utilisées par le script d'installation de la base de données ``install_db.sh``. L'utilisateurs PostgreSQL doit être en concordance avec celui créé lors de la dernière étape de l'installation serveur ``Création d'un utilisateur PostgreSQL``. 

:notes:

    Si vous installer UsersHub dans le cadre de la gestion des utilisateurs de GeoNature, il est conseillé d'utiliser les mêmes utilisateurs PostgreSQL que pour GeoNature.



Création de la base de données
==============================

* Création de la base de données et chargement des données initiales
 
  ::  
  
    cd /home/synthese/usershub
    sudo ./install_db.sh

Configuration de l'application
==============================

* Se loguer sur le serveur avec l'utilisateur linux ``synthese``
   

* Installation et configuration de l'application
 
  ::  
  
    cd /home/synthese/usershub
    ./install_app.sh

Vous devez éditer le fichier dbconnexoins.json et y ajouter les paramètres de connexions à toutes les bases que vous souhaitez synchroniser avec UsersHub.
Si vous avez changer l'utilisateur et le mot de passe par défaut, vous devez changer la première section de ce fichier pour obtenir quelque chose qui ressemble à ceci :
 
::  
  
    ...
    "dbfunname":"Utilisateurs"
    ,"host":"localhost"
    ,"dbname":"usershubdb"
    ,"user":"geonatuser"
    ,"pass":"monpassachanger"
    ...

UsersHub peut fonctionner seul avec sa propre base de données mais il est configurer par défaut pour fonctionner avec GeoNature. Vous devez renseigner les paramêtres de connexion à la base de GeoNature.

* Pour tester, se connecter à l'application via http://mon-domaine.fr/usershub et les login et pass admin/admin

* choisir le mode d'authentification dans le fichier ``config/config.php``

Mise à jour de l'application
----------------------------

* Suivre les instructions disponibles dans la doc de la release choisie

Personnalisation
----------------

Vous pouvez changer le bandeau de l'application en remplaçant le fichier ``web/images/bandeau_utilisateurs.png`` par un bandeau personnalisé.

Vous pouvez changer le logo de l'application en remplaçant le fichier ``web/images/main_logo.png`` une image de votre choix.
