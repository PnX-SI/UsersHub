.. image:: http://geonature.fr/img/logo-pne.jpg
    :target: http://www.ecrins-parcnational.fr
    
=======
SERVEUR
=======

Cette documentation décrit l'installation indépendante de UsersHub. Il est aussi possible de réaliser l'installation avec le script automatisé d'installation globale de GeoNature (https://github.com/PnEcrins/GeoNature/tree/master/docs/install_all).

Prérequis
=========

* Ressources minimum du serveur :

Un serveur disposant d'au moins de 1 Go RAM et de 5 Go d'espace disque.

* Disposer d'un utilisateur linux (nommé ``synthese`` dans notre exemple). Le répertoire de cet utilisateur ``synthese`` doit être dans ``/home/synthese``. Si vous souhaitez utiliser un autre utilisateur linux, vous devrez adapter les lignes de commande proposées dans cette documentation.
 
  ::  
  
    # adduser --home /home/synthese synthese
    # adduser synthese sudo

:Note:

    Pour la suite de l'installation, veuillez utiliser l'utilisateur Linux créé précedemment (``synthese`` dans l'exemple), et non l'utilisateur ``root``.

* Récupérer le zip de l'application sur le Github du projet (X.Y.Z à remplacer par la version souhaitée de UsersHub)
 
  ::  
  
    $ cd /home/synthese
    $ wget https://github.com/PnX-SI/UsersHub/archive/X.Y.Z.zip
    $ unzip X.Y.Z.zip
    $ mv UsersHub-X.Y.Z usershub


Installation et configuration du serveur
========================================

Installation pour Debian 10 et Debian 11.

::  
  
    $ sudo apt install -y python3-venv libpq-dev postgresql apache2
    
* Installer NVM (Node version manager), node et npm

::  
        
    $ wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

 
Fermer la console et la réouvrir pour que l’environnement npm soit pris en compte.


Installation et configuration de PostgreSQL
===========================================

* Installation de PostgreSQL
 
  ::  
  
    $ sudo apt-get install postgresql

* Création d'un utilisateur PostgreSQL
 
  ::  
  
    $ sudo -u postgres psql -c "CREATE ROLE geonatuser WITH LOGIN PASSWORD 'monpassachanger';"
