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
  
    sudo adduser --home /home/synthese synthese


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

:notes:

    Cette documentation concerne une installation sur Debian. Pour tout autre environemment les commandes sont à adapter.



:notes:

    Bien qu'indépendante, cette documentation est en lien avec l'installation de GeoNature : https://github.com/PnEcrins/GeoNature.

::

    sudo apt-get install apache2  python-dev python-pip libpq-dev supervisor
    adduser synthese sudo
    exit
    
Fermer la console et la réouvrir pour que les modifications soient prises en compte.
    


Installation et configuration de PosgreSQL
==========================================



* Installation de PostreSQL
 
  ::  
  
    sudo apt-get install postgresql-9.6 postgresql-server-dev-9.6
    sudo adduser postgres sudo
        
