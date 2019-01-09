.. image:: http://geonature.fr/img/logo-pne.jpg
    :target: http://www.ecrins-parcnational.fr
    
=======
SERVEUR
=======

Cette documentation décrit l'installation indépendante de UsersHub. Il est aussi possible de l'installation avec le script automatisé d'installation globale de GeoNature (https://github.com/PnEcrins/GeoNature/tree/master/docs/install_all).

Prérequis
=========

* Ressources minimum serveur :

Un serveur disposant d'au moins de 1 Go RAM et de 5 Go d'espace disque.

* Disposer d'un utilisateur linux (nommé ``synthese`` dans notre exemple). Le répertoire de cet utilisateur ``synthese`` doit être dans ``/home/synthese``. Si vous souhaitez utiliser un autre utilisateur linux, vous devrez adapter les lignes de commande proposées dans cette documentation ainsi que dans les fichiers ``install_db.sh`` et ``install_app.sh``
 
  ::  
  
    adduser --home /home/synthese synthese

:Note:

    Pour la suite de l'installation, veuillez utiliser l'utilisateur Linux créer précedemment (``synthese``), et non l'utilisateur ``root``.

* Récupérer le zip de l'application sur le Github du projet (X.Y.Z à remplacer par la version souhaitée de UsersHub)
 
  ::  
  
    cd /tmp
    wget https://github.com/PnEcrins/UsersHub/archive/vX.Y.Z.zip
    unzip vX.Y.Z.zip
    mkdir -p /home/synthese/usershub
    cp usershub-X.Y.Z/* /home/synthese/usershub
    cd /home/synthese


Installation et configuration du serveur
========================================

Installation pour Debian 9.

::  
  
    su -
    apt-get install apache2  python-dev python-pip libpq-dev supervisor
    adduser synthese sudo
    
Fermer la console et la réouvrir pour que les modifications soient prises en compte.
    
:Note:

    Cette documentation concerne une installation sur Debian. Pour tout autre environemment les commandes sont à adapter.

Installation et configuration de PostgreSQL
===========================================

* Installation de PostgreSQL
 
  ::  
  
    apt-get install postgresql-9.6 postgresql-server-dev-9.6
    adduser postgres sudo
    exit
