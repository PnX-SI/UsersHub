#!/usr/bin/env bash
# Make sure root cannot run our script
if [ "$(id -u)" == "0" ]; then
    echo "This script must NOT be run as root" 1>&2
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
        PGPASSWORD=$user_pg_pass psql -h $db_host -p $pg_port -U $user_pg -tAl | grep -q "^$1|"
        return $?
    fi
}

if database_exists $db_name
then
    if $drop_apps_db
    then
        echo "Suppression de la base..."
        PGPASSWORD=$user_pg_pass dropdb -U $user_pg -h $db_host -p $pg_port $db_name
    else
        echo "La base de données existe et le fichier de settings indique de ne pas la supprimer."
    fi
fi

if ! database_exists $db_name
then
    mkdir -p log
    echo "Création de la base..."
    PGPASSWORD=$user_pg_pass createdb -h $db_host -p $pg_port -U $user_pg -O $user_pg $db_name
    echo "Ajout de l'extension pour les UUID..."
    PGPASSWORD=$user_pg_pass psql -h $db_host -p $pg_port -U $user_pg -d $db_name -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
fi


source venv/bin/activate
flask db upgrade usershub@head
flask db upgrade utilisateurs@head
deactivate
