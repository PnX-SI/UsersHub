CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--Update t_roles TABLE
DO $$ 
    BEGIN
        ALTER TABLE utilisateurs.t_roles ADD COLUMN uuid_role uuid;
    EXCEPTION
        WHEN duplicate_column THEN RAISE NOTICE 'column "uuid_role" already exists in "utilisateurs.t_roles".';
    END
$$;

ALTER TABLE utilisateurs.t_roles DROP COLUMN IF EXISTS pass_sha;

DO $$ 
    BEGIN
        ALTER TABLE utilisateurs.t_roles ADD COLUMN pass_plus text;
    EXCEPTION
        WHEN duplicate_column THEN RAISE NOTICE 'column "pass_plus" already exists in "utilisateurs.t_roles".';
    END
$$;

--Update bib_organismes TABLE
DO $$ 
    BEGIN
        ALTER TABLE utilisateurs.bib_organismes ADD COLUMN uuid_organisme uuid;
    EXCEPTION
        WHEN duplicate_column THEN RAISE NOTICE 'column "uuid_organisme" already exists in "utilisateurs.bib_organismes".';
    END
$$;
