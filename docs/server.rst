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
  
    adduser --home /home/synthese synthese
    adduser synthese sudo

:Note:

    Pour la suite de l'installation, veuillez utiliser l'utilisateur Linux créé précedemment (``synthese`` dans l'exemple), et non l'utilisateur ``root``.

* Récupérer le zip de l'application sur le Github du projet (X.Y.Z à remplacer par la version souhaitée de UsersHub)
 
  ::  
  
    cd /home/synthese
    wget https://github.com/PnX-SI/UsersHub/archive/X.Y.Z.zip
    unzip X.Y.Z.zip
    mv UsersHub-X.Y.Z usershub


Installation et configuration du serveur
========================================

Installation pour Debian 9.

::  
  
    sudo apt-get install -y python3 python3-dev python3-setuptools python-pip python-virtualenv libpq-dev 
    sudo apt-get install -y supervisor
    sudo apt-get install -y apache2
    sudo apt-get install -y curl
    curl -sL https://deb.nodesource.com/setup_10.x | bash -
    sudo apt-get install -y nodejs 
    pip install virtualenv==20.0.1
    
* Installer NVM (Node version manager), node et npm

  ::  
        
        wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.33.6/install.sh | bash

        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

 
Fermer la console et la réouvrir pour que les modifications soient prises en compte.
    
:Note:

    Cette documentation concerne une installation sur Debian. Pour tout autre environemment les commandes sont à adapter.

Installation et configuration de PostgreSQL
===========================================

* Installation de PostgreSQL
 
  ::  
  
    sudo apt-get install postgresql-9.6 postgresql-server-dev-9.6

* Création d'un utilisateur PostgreSQL
 
  ::  
  
    sudo su postgres
    psql
    CREATE ROLE geonatuser WITH LOGIN PASSWORD 'monpassachanger';
    \q
    exit
