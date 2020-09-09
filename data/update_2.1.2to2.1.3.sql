\echo 'Update UsersHub DB schema to v2.1.3'
BEGIN;

\echo '----------------------------------------------------------------------------'
\echo 'Add confirmation_url field to temp_users table'
ALTER TABLE utilisateurs.temp_users ADD confirmation_url varchar(250) NULL;

COMMIT;