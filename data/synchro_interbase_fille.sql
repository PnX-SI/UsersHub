-- SUR LA BASE FILLE
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

CREATE SERVER my_db_server
    FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'localhost', dbname 'my_db', port '5432');

CREATE USER MAPPING
    FOR test
    SERVER my_db_server
    OPTIONS (password 'test', user 'test');

DROP SCHEMA IF EXISTS fdw_utilisateurs CASCADE;
CREATE SCHEMA IF NOT EXISTS fdw_utilisateurs;

IMPORT FOREIGN SCHEMA utilisateurs
    FROM SERVER my_db_server INTO fdw_utilisateurs;
