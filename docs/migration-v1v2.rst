=================
MIGRATION V1 > V2
=================

Procédure de mise à jour de UsersHub version 1 vers la version 2.0.0

* Télécharger la dernière version de UsersHub
 
  ::  
  
    cd
    wget https://github.com/PnEcrins/UsersHub/archive/X.Y.Z.zip
    unzip X.Y.Z.zip
    rm X.Y.Z.zip

Renommer l’ancien repertoire de l’application, ainsi que le nouveau :

::  
  
    mv /home/`whoami`/usershub/ /home/`whoami`/usershub_old/
    mv UsersHub-X.Y.Z /home/`whoami`/usershub/

* Créer et mettre à jour le fichier ``config/settings.ini``.

Remplir uniquement la partie 'PostgreSQL settings' et 'Application settings', avec les paramètres de connexion de la base de données contenant votre schéma ``utilisateurs``. Dans notre cas, il s'agit de la base de données de GeoNature.
 
::  
  
    cd usershub
    cp config/settings.ini.sample config/settings.ini
    nano config/settings.ini

Exemple :

::

    # Effacer la base de donnée existante lors de l'installation
    drop_apps_db=false
    # Host de la base de données de l'application
    db_host=localhost
    # Port du serveur PostgreSQL
    pg_port=5432
    # Nom de la base de données de l'application
    db_name=geonature2db
    # Nom de l'utilisateur propriétaire de la BDD de l'application
    user_pg=geonatadmin 
    # User propriétaire de la BDD de l'application
    user_pg_pass=monpassachanger
    # Intégrer les données minimales (Applications et tags)
    insert_minimal_data=true
    # Intégrer les données exemple (Role, groupe, organismes et correspondances)
    insert_sample_data=true
    # URL de l'application
    url_application=http://test.ecrins-parcnational.net/usershub


Passer le script de migration ``data/update_1.3.3to2.0.0.sql``

Lancer le script d'installation de l'application :

::

    ./install_app.sh


* Configuration Apache

Supprimer le contenu du fichier ``/etc/apache2/sites-enabled/usershub.conf`` et le remplacer par les lignes suivantes :
 
::  
  
    <Location /usershub>
        ProxyPass  http://localhost:5001/
        ProxyPassReverse  http://localhost:5001/
    </Location>

Redémarer Apache
 
::  
  
    sudo service apache2 restart
