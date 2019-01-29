===========
APPLICATION
===========

:Note:

    Pour la suite de l'installation, veuillez utiliser l'utilisateur Linux créer précedemment (``synthese``), et non l'utilisateur ``root``.

Configuration de la base de données PostgreSQL
==============================================

* Créer et mettre à jour le fichier ``config/settings.ini``
 
  ::  
  
    cp config/settings.ini.sample config/settings.ini
    nano config/settings.ini

Renseigner le nom de la base de données, l'utilisateur PostgreSQL et son mot de passe. Il est possible mais non conseillé de laisser les valeurs proposées par défaut. 

ATTENTION : Les valeurs renseignées dans ce fichier sont utilisées par le script d'installation de la base de données ``install_db.sh``. L'utilisateurs PostgreSQL doit être en concordance avec celui créé lors de la dernière étape de l'installation serveur ``Création d'un utilisateur PostgreSQL``. 

:Note:

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


Configuration Apache
====================

Créer le fichier ``/etc/apache2/sites-avalaible/usershub.conf`` avec ce contenu :
 
::  
  
    <Location /usershub2>
        ProxyPass  http://localhost:5001
        ProxyPassReverse  http://localhost:5001
    </Location>

Activer le site et recharger la conf Apache :
 
::  
  
    sudo a2ensite usershub
    sudo service apache2 restart

UsersHub peut fonctionner seul avec sa propre base de données mais il est configuré par défaut pour fonctionner avec GeoNature. Vous devez renseigner les paramêtres de connexion à la base de GeoNature.

* Pour tester, se connecter à l'application via http://mon-domaine.fr/usershub et les login et pass admin/admin


Mise à jour de l'application
============================

* Télécharger la dernière version de UsersHub

::

    wget https://github.com/PnEcrins/UsersHub/archive/X.Y.Z.zip
    unzip X.Y.Z.zip
    rm X.Y.Z.zip

* Renommer l’ancien repertoire de l’application, ainsi que le nouveau :

::

    mv /home/`whoami`/usershub/ /home/`whoami`/usershub_old/
    mv UsersHub-X.Y.Z /home/`whoami`/usershub/

* Récupérer les fichiers de configuration de la version précedente :

::

    cp /home/`whoami`/usershub_old/config/config.py /home/`whoami`/usershub/config/config.py
    cp /home/`whoami`/usershub_old/config/settings.ini /home/`whoami`/usershub/config/settings.ini 

* Lancer le script d'installation de l'application :

::
    
    cd usershub
    ./install_app.sh

* Suivre les éventuelles notes de version spécifique à chaque version
