#!/bin/bash
# Make sure root cannot run our script
if [ "$(id -u)" == "0" ]; then
   echo "This script must NOT be run as root" 1>&2
   exit 1
fi

. config/settings.ini

sudo service postgresql restart
function database_exists () {
    # /!\ Will return false if psql can't list database. Edit your pg_hba.conf
    # as appropriate.
    if [ -z $1 ]
    then
        # Argument is null
        return 0
    else
        # Grep db name in the list of database
        sudo -n -u postgres -s -- psql -tAl | grep -q "^$1|"
        return $?
    fi
}

if database_exists $db_name
then
    if $drop_apps_db
        then
        echo "Suppression de la base..."
        sudo -n -u postgres -s dropdb $db_name
    else
        echo "La base de données existe et le fichier de settings indique de ne pas la supprimer."
    fi
fi

if ! database_exists $db_name
then
    mkdir -p log
    echo "Création de la base..."
    sudo -n -u postgres -s createdb -O $user_pg $db_name
    echo "Ajout du language plpgsql et de l'extension pour les UUID..."
    sudo -n -u postgres -s psql -d $db_name -c "CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog; COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';"
    sudo -n -u postgres -s psql -d $db_name -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
    # Mise en place de la structure de la base et des données permettant son fonctionnement avec l'application
    echo "Création de la structure de la base de données..."
    export PGPASSWORD=$user_pg_pass;psql -h $db_host -U $user_pg -d $db_name -f data/usershub.sql &>> log/install_db.log
    if $insert_minimal_data
        then
            echo "Insertion des données minimales dans la base de données..."
            export PGPASSWORD=$user_pg_pass;psql -h $db_host -U $user_pg -d $db_name -f data/usershub-data.sql &>> log/install_db.log
    fi
    if $insert_sample_data
        then
            echo "Insertion des données exemple dans la base de données..."
            export PGPASSWORD=$user_pg_pass;psql -h $db_host -U $user_pg -d $db_name -f data/usershub-dataset.sql &>> log/install_db.log
    fi
fi
