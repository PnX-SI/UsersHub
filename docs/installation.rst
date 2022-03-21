============
INSTALLATION
============

Cette documentation décrit l'installation indépendante de UsersHub. Il est aussi possible de réaliser l'installation avec le script automatisé d'installation globale de GeoNature (http://docs.geonature.fr/installation.html#installation-globale).

Prérequis
=========

Pour installer UsersHub, il vous faut un serveur avec :

* Debian 10 ou 11
* 1 Go de RAM
* 5 Go d’espace disque

Création d’un utilisateur
=========================

Vous devez disposer d'un utilisateur Linux pour faire tourner UsersHub (nommé ``synthese`` dans notre exemple). L’utilisateur doit appartenir au groupe ``sudo``. Le répertoire de cet utilisateur ``synthese`` doit être dans ``/home/synthese``. Si vous souhaitez utiliser un autre utilisateur Linux, vous devrez adapter les lignes de commande proposées dans cette documentation.

::

    $ adduser --home /home/synthese synthese
    $ adduser synthese sudo

:Note:

    Pour la suite de l'installation, veuillez utiliser l'utilisateur Linux créé précedemment (``synthese`` dans l'exemple), et non l'utilisateur ``root``.

Installation des dépendances requises
=====================================

Installez les dépendances suivantes :

::

    $ sudo apt install -y python3-venv libpq-dev postgresql apache2

Installer NVM (Node version manager), Node.js et npm :

::

    $ wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

Fermer la console et la réouvrir pour que l’environnement npm soit pris en compte.

Configuration de PostgresQL
===========================

Créer un utilisateur PostgreSQL :

::

    $ sudo -u postgres psql -c "CREATE ROLE geonatuser WITH LOGIN PASSWORD 'monpassachanger';"

Téléchargement de UsersHub
==========================

Récupérer le zip de l'application sur le Github du projet (X.Y.Z à remplacer par la version souhaitée de UsersHub)

::

    $ cd /home/synthese
    $ wget https://github.com/PnX-SI/UsersHub/archive/X.Y.Z.zip
    $ unzip X.Y.Z.zip
    $ mv UsersHub-X.Y.Z usershub

Configuration de UsersHub
=========================

Créer et mettre à jour le fichier ``config/settings.ini`` :
 
::  
  
    $ cd ~/usershub
    $ cp config/settings.ini.sample config/settings.ini
    $ nano config/settings.ini

Renseigner le nom de la base de données, l'utilisateur PostgreSQL et son mot de passe. Il est possible mais non conseillé de laisser les valeurs proposées par défaut. 

ATTENTION : Les valeurs renseignées dans ce fichier sont utilisées par le script d'installation de la base de données ``install_db.sh``. L'utilisateurs PostgreSQL doit être en concordance avec celui créé lors de la dernière étape de l'installation du serveur (``Création d'un utilisateur PostgreSQL``). 

:Note:

    Si vous installez UsersHub dans le cadre de la gestion des utilisateurs de GeoNature, il est conseillé d'utiliser les mêmes utilisateurs PostgreSQL que pour GeoNature.


Configuration de l'application
==============================

* Installation de l'application :

::
  
    cd ~/usershub
    ./install_app.sh


Création et installation de la base de données
==============================================

* Création de la base de données et chargement des données initiales :
 
::  
  
    cd ~/usershub
    ./install_db.sh


* Si vous souhaitez les données utilisateurs d’exemple, en particulier l’utilisateur ``admin`` (mot de passe : ``admin``), executez :

::

    cd ~/usershub
    source venv/bin/activate
    flask db upgrade usershub-samples@head


Configuration Apache
====================

Activez les modules ``mod_proxy`` et ``mod_proxy_http``, et redémarrez Apache :

::

    $ sudo a2enmod proxy proxy_http
    $ sudo systemctl restart apache

UsersHub peut être classiquement déployé sur 2 types d’URL distincts :

* Sur un préfixe : https://mon-domaine.fr/usershub/
* Sur un sous-domaine : https://usershub.mon-domaine.fr

Installation de UsersHub sur un préfixe
---------------------------------------

Le processus d’installation de l’application créer le fichier de configuration Apache ``/etc/apache2/conf-available/usershub.conf`` permettant de servir UsersHub sur le préfixe ``/usershub/``. Pour activer ce fichier de configuration, exécutez les commandes suivantes :
 
::  
  
    sudo a2enconf usershub
    sudo service apache2 reload

Installation de UsersHub sur un sous-domaine
--------------------------------------------

Dans le cas où UsersHub est installé sur un sous-domaine et non sur un préfixe (c’est-à-dire ``https://usershub.mon-domaine.fr``), veuillez ajouter dans le fichier de configuration de votre virtualhost (*e.g.* ``/etc/apache2/sites-enabled/usershub.conf``) la section suivante :

::

    <Location />
        ProxyPass http://127.0.0.1:5001/
        ProxyPassReverse http://127.0.0.1:5001/
    </Location>


Mise à jour de l'application
============================

* Télécharger la dernière version de UsersHub

::

    cd
    wget https://github.com/PnX-SI/UsersHub/archive/X.Y.Z.zip
    unzip X.Y.Z.zip
    rm X.Y.Z.zip

* Renommer l’ancien répertoire de l’application, ainsi que le nouveau :

::

    mv /home/`whoami`/usershub/ /home/`whoami`/usershub_old/
    mv UsersHub-X.Y.Z /home/`whoami`/usershub/

* Récupérer les fichiers de configuration de la version précedente :

::

    cp /home/`whoami`/usershub_old/config/config.py /home/`whoami`/usershub/config/config.py
    cp /home/`whoami`/usershub_old/config/settings.ini /home/`whoami`/usershub/config/settings.ini 

* Lancer le script d'installation de l'application (attention si vous avez modifiez certains paramètres dans le fichier ``config.py`` tels que les paramètres de connexion à la base de données, ils seront écrasés par les paramètres présent dans le fichier ``settings.ini``) :

::
    
    cd usershub
    ./install_app.sh

* Mettre à jour la base de données :

::

    cd usershub
    source venv/bin/activate
    flask db upgrade usershub@head

* Suivre les éventuelles notes de version spécifiques à chaque version
