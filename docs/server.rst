.. image:: http://geotrek.fr/images/logo-pne.png
    :target: http://www.ecrins-parcnational.fr
    
=======
SERVEUR
=======


Prérequis
=========

* Ressources minimum serveur :

Un serveur disposant d'au moins de 1 Go RAM et de 5 Go d'espace disque.


* disposer d'un utilisateur linux nommé ``synthese``. Le répertoire de cet utilisateur ``synthese`` doit être dans ``/home/synthese``
Si vous souhaitez utiliser un autre utilisateur linux, vous devrez adapter les lignes de commande proposer dans cette documentation ainsi que dans les fichiers ``install_db.sh`` et ``install_app.sh``

    :: 
    
        sudo adduser --home /home/synthese synthese


* récupérer le zip de l'application sur le Github du projet

    ::
    
        cd /tmp
        wget https://github.com/PnEcrins/UsersHub/archive/vX.Y.Z.zip
        unzip vX.Y.Z.zip
        mkdir -p /home/synthese/usershub
        cp usershub-X.Y.Z/* /home/synthese/usershub
        cd /home/synthese


Installation et configuration du serveur
========================================

Installation pour Debian 7.

:notes:

    Cette documentation concerne une installation sur Debian. Pour tout autre environemment les commandes sont à adapter.

.

:notes:

    Bien qu'indépendante, cette documentation est en lien avec l'installation de geonature : https://github.com/PnEcrins/GeoNature.

.

  ::
  
    su - 
    apt-get install apache2 php5 libapache2-mod-php5 php5-gd libapache2-mod-wsgi php5-pgsql sudo
    usermod -g www-data synthese
    usermod -a -G root synthese
    adduser synthese sudo
    exit
    
    Fermer la console et la réouvrir pour que les modifications soient prises en compte
    
* Ajouter un alias du serveur de base de données dans le fichier /etc/hosts

  ::  
        
        sudo sh -c 'echo "127.0.1.1       databases" >> /etc/hosts'
        sudo apache2ctl restart

:notes:

    Cet alias ``databases`` permet d'identifier sur quel host l'application doit rechercher la base de données PostgreSQL
    
    Par défaut, PostgreSQL est en localhost (127.0.1.1)
    
    Si votre serveur PostgreSQL est sur un autre host (par exemple sur ``50.50.56.27``), vous devez modifier la chaine de caratères ci-dessus comme ceci ``50.50.56.27   databases``

* Vérifier que le répertoire ``/tmp`` existe et que l'utilisateur ``www-data`` y ait accès en lecture/écriture

Installation et configuration de PosgreSQL
==========================================

* Sur Debian 7, configuration des dépots pour avoir les dernières versions de PostgreSQL (9.3) et PostGIS (2.1)
(http://foretribe.blogspot.fr/2013/12/the-posgresql-and-postgis-install-on.html)

  ::  
  
        sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main" >> /etc/apt/sources.list'
        sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
        sudo apt-get update

* Installation de PostreSQL

    ::
    
        sudo apt-get install postgresql-9.3 postgresql-client-9.3
        sudo adduser postgres sudo
        
* configuration PostgreSQL - permettre l'écoute de toutes les ip

    ::
    
        sed -e "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" -i /etc/postgresql/9.3/main/postgresql.conf
        sudo sed -e "s/# IPv4 local connections:/# IPv4 local connections:\nhost\tall\tall\tde.la.merde.0\/33\t md5/g" -i /etc/postgresql/9.3/main/pg_hba.conf
        /etc/init.d/postgresql restart

* Création d'un super-utilisateur PostgreSQL

    ::
    
        sudo su postgres
        psql
        CREATE ROLE usershubadmin WITH SUPERUSER LOGIN PASSWORD 'monpassachanger';
        \q
        exit
        
L'utilisateur ``geonatuser`` sera le propriétaire de la base de données ``geonaturedb`` et sera utilisé par l'application pour se connecter à celle-ci.

L'utilisateur ``geonatadmin`` est super utilisateur de PostgreSQL il sera utilisé par l'application pour se connecter à sa propre base de données mais aussi à toutes les autres bases qu'UsersHub doit gérer.

L'application fonctionne avec par default le mot de passe ``monpassachanger`` mais il est conseillé de le modifier !

Ce mot de passe, ainsi que l'utilisateur PostgreSQL ``geonatadmin`` créés ci-dessus sont des valeurs par défaut utiliser à plusieurs reprises dans l'application. Ils peuvent cependant être changés. S'ils doivent être changés, ils doivent l'être dans plusieurs fichiers de l'application : 

    config/settings.ini
    
    config/connecter.php
    
    config/dbconnexions.json
    
