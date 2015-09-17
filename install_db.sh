#!/bin/bash
# Make sure only root can run our script
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

. config/settings.ini


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
    echo "Ajout du language plpgsql..."
    sudo -n -u postgres -s psql -d $db_name -c "CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog; COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';"
    # Mise en place de la structure de la base et des données permettant son fonctionnement avec l'application
    echo "Création de la base..."
    export PGPASSWORD=$user_pg_pass;psql -h databases -U $user_pg -d $db_name -f data/usershub.sql &>> log/install_db.log
fi
