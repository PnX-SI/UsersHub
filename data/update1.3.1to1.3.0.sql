--Nettoyage
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

--Update t_roles TABLE
ALTER TABLE utilisateurs.t_roles ADD COLUMN uuid_role uuid;
ALTER TABLE utilisateurs.t_roles ALTER COLUMN uuid_role SET DEFAULT public.uuid_generate_v4(); 
UPDATE utilisateurs.t_roles SET uuid_role = public.uuid_generate_v4();
ALTER TABLE utilisateurs.t_roles ALTER COLUMN uuid_role SET NOT NULL;

ALTER TABLE utilisateurs.t_roles ADD COLUMN pass_plus text;


--Update bib_organismes TABLE
ALTER TABLE utilisateurs.bib_organismes ADD COLUMN uuid_organisme uuid;
ALTER TABLE utilisateurs.bib_organismes ALTER COLUMN uuid_organisme SET DEFAULT public.uuid_generate_v4(); 
UPDATE utilisateurs.bib_organismes SET uuid_organisme = public.uuid_generate_v4();
ALTER TABLE utilisateurs.bib_organismes ALTER COLUMN uuid_organisme SET NOT NULL;