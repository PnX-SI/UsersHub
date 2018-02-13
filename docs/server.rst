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

Installation pour Debian 7.

:notes:

    Cette documentation concerne une installation sur Debian. Pour tout autre environemment les commandes sont à adapter.



:notes:

    Bien qu'indépendante, cette documentation est en lien avec l'installation de GeoNature : https://github.com/PnEcrins/GeoNature.

::

    su - 
    apt-get install apache2 php5 libapache2-mod-php5 php5-gd libapache2-mod-wsgi php5-pgsql sudo
    usermod -g www-data synthese
    usermod -a -G root synthese
    adduser synthese sudo
    exit
    
Fermer la console et la réouvrir pour que les modifications soient prises en compte.
    

* Vérifier que le répertoire ``/tmp`` existe et que l'utilisateur ``www-data`` y ait accès en lecture/écriture

Installation et configuration de PosgreSQL
==========================================

* Sur Debian 7, configuration des dépots pour avoir les dernières versions de PostgreSQL (9.3) et PostGIS (2.1) (voir http://foretribe.blogspot.fr/2013/12/the-posgresql-and-postgis-install-on.html)
 
  ::  
  
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ wheezy-pgdg main" >> /etc/apt/sources.list'
    sudo wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update

* Installation de PostreSQL
 
  ::  
  
    sudo apt-get install postgresql-9.3 postgresql-client-9.3
    sudo adduser postgres sudo
        
* Configuration de PostgreSQL - permettre l'écoute de toutes les IP
 
  ::  
  
    sed -e "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" -i /etc/postgresql/9.3/main/postgresql.conf
    sudo sed -e "s/# IPv4 local connections:/# IPv4 local connections:\nhost\tall\tall\tde.la.merde.0\/33\t md5/g" -i /etc/postgresql/9.3/main/pg_hba.conf
    /etc/init.d/postgresql restart

* Création d'un super-utilisateur PostgreSQL
 
  ::  
  
    sudo su postgres
    psql
    CREATE ROLE geonatuser WITH LOGIN PASSWORD 'monpassachanger';
    \q
    exit

L'utilisateur ``geonatuser`` est super utilisateur de PostgreSQL il sera utilisé par l'application pour se connecter à sa propre base de données mais aussi à toutes les autres bases qu'UsersHub doit gérer.

L'application fonctionne avec par default le mot de passe ``monpassachanger`` mais il est conseillé de le modifier !

Ce mot de passe, ainsi que l'utilisateur PostgreSQL ``geonatuser`` créés ci-dessus sont des valeurs par défaut utiliser à plusieurs reprises dans l'application. Ils peuvent cependant être changés. S'ils doivent être changés, ils doivent l'être dans plusieurs fichiers de l'application : 

- config/settings.ini
- config/connecter.php
- config/dbconnexions.json

Configuration Apache
=====================

Créer le fichier de configuration Apache pour UsersHub:

``sudo touch /etc/apache2/sites-available/usershub.conf``

Ouvrir et copier la configuration suivante dans le fichier créé:

``sudo nano usershub.conf`` 

  ::  
  
    #Configuration usershub
    Alias /usershub /home/<MON_USER>/usershub/web
    <Directory /home/<MON_USER>/usershub/web>
    Require all granted
    </Directory>


    
