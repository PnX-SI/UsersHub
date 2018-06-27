SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

CREATE SCHEMA IF NOT EXISTS utilisateurs;

SET search_path = utilisateurs, pg_catalog;

CREATE OR REPLACE FUNCTION modify_date_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.date_insert := now();
    NEW.date_update := now();
    RETURN NEW;
END;
$$;

CREATE OR REPLACE FUNCTION modify_date_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.date_update := now();
    RETURN NEW;
END;
$$;

SET default_tablespace = '';
SET default_with_oids = false;

CREATE TABLE IF NOT EXISTS cor_roles (
    id_role_groupe integer NOT NULL,
    id_role_utilisateur integer NOT NULL
);

CREATE TABLE IF NOT EXISTS t_roles (
    groupe boolean DEFAULT false NOT NULL,
    id_role integer NOT NULL,
    uuid_role uuid NOT NULL DEFAULT public.uuid_generate_v4(),
    identifiant character varying(100),
    nom_role character varying(50),
    prenom_role character varying(50),
    desc_role text,
    pass character varying(100),
    pass_plus text,
    email character varying(250),
    id_organisme integer,
    id_unite integer,
    remarques text,
    pn boolean,
    session_appli character varying(50),
    date_insert timestamp without time zone,
    date_update timestamp without time zone
);

CREATE SEQUENCE t_roles_id_role_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
ALTER SEQUENCE t_roles_id_role_seq OWNED BY t_roles.id_role;
ALTER TABLE ONLY t_roles ALTER COLUMN id_role SET DEFAULT nextval('t_roles_id_role_seq'::regclass);

CREATE TABLE IF NOT EXISTS bib_organismes (
    uuid_organisme uuid NOT NULL DEFAULT public.uuid_generate_v4(),
    nom_organisme character varying(100) NOT NULL,
    adresse_organisme character varying(128),
    cp_organisme character varying(5),
    ville_organisme character varying(100),
    tel_organisme character varying(14),
    fax_organisme character varying(14),
    email_organisme character varying(100),
    id_organisme integer NOT NULL,
    id_parent integer
);

CREATE SEQUENCE bib_organismes_id_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
ALTER SEQUENCE bib_organismes_id_seq OWNED BY bib_organismes.id_organisme;
ALTER TABLE ONLY bib_organismes ALTER COLUMN id_organisme SET DEFAULT nextval('bib_organismes_id_seq'::regclass);

CREATE TABLE IF NOT EXISTS bib_unites (
    nom_unite character varying(50) NOT NULL,
    adresse_unite character varying(128),
    cp_unite character varying(5),
    ville_unite character varying(100),
    tel_unite character varying(14),
    fax_unite character varying(14),
    email_unite character varying(100),
    id_unite integer NOT NULL
);

CREATE SEQUENCE bib_unites_id_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
ALTER SEQUENCE bib_unites_id_seq OWNED BY bib_unites.id_unite;
ALTER TABLE ONLY bib_unites ALTER COLUMN id_unite SET DEFAULT nextval('bib_unites_id_seq'::regclass);

CREATE TABLE IF NOT EXISTS utilisateurs.cor_role_tag_application (
    id_role integer NOT NULL,
    id_tag integer NOT NULL,
    id_application integer NOT NULL
);

CREATE TABLE IF NOT EXISTS t_applications (
    id_application integer NOT NULL,
    nom_application character varying(50) NOT NULL,
    desc_application text,
    id_parent integer
);

CREATE SEQUENCE t_applications_id_application_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
ALTER SEQUENCE t_applications_id_application_seq OWNED BY t_applications.id_application;
ALTER TABLE ONLY t_applications ALTER COLUMN id_application SET DEFAULT nextval('t_applications_id_application_seq'::regclass);

CREATE TABLE IF NOT EXISTS t_tags (
    id_tag integer NOT NULL,
    id_tag_type integer NOT NULL,
    tag_code character varying(25),
    tag_name character varying(255),
    tag_label character varying(255),
    tag_desc text,
    date_insert timestamp without time zone,
    date_update timestamp without time zone
);
COMMENT ON TABLE t_tags IS 'Permet de créer des étiquettes ou tags ou labels, qu''il est possible d''attacher à différents objects de la base. Cela peut permettre par exemple de créer des groupes ou des listes d''utilisateurs';

CREATE SEQUENCE t_tags_id_tag_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
ALTER SEQUENCE t_tags_id_tag_seq OWNED BY t_tags.id_tag;
ALTER TABLE ONLY t_tags ALTER COLUMN id_tag SET DEFAULT nextval('t_tags_id_tag_seq'::regclass);

CREATE TABLE IF NOT EXISTS bib_tag_types (
    id_tag_type integer NOT NULL,
    tag_type_name character varying(100) NOT NULL,
    tag_type_desc character varying(255) NOT NULL
);
COMMENT ON TABLE bib_tag_types IS 'Permet de définir le type du tag';

CREATE TABLE IF NOT EXISTS cor_tags_relations (
    id_tag_l integer NOT NULL,
    id_tag_r integer NOT NULL,
    relation_type character varying(255) NOT NULL
);
COMMENT ON TABLE cor_tags_relations IS 'Permet de définir des relations nn entre tags en affectant des étiquettes à des tags';

CREATE TABLE IF NOT EXISTS cor_role_tag (
    id_role integer NOT NULL,
    id_tag integer NOT NULL
);
COMMENT ON TABLE cor_role_tag IS 'Permet d''attacher des étiquettes à des roles. Par exemple pour créer des listes d''observateurs';

CREATE TABLE IF NOT EXISTS cor_organism_tag (
    id_organism integer NOT NULL,
    id_tag integer NOT NULL
);
COMMENT ON TABLE cor_organism_tag IS 'Permet d''attacher des étiquettes à des organismes';

CREATE TABLE IF NOT EXISTS cor_application_tag (
    id_application integer NOT NULL,
    id_tag integer NOT NULL
);
COMMENT ON TABLE cor_organism_tag IS 'Permet d''attacher des étiquettes à des applications';

CREATE TABLE IF NOT EXISTS cor_app_privileges (
    id_tag_action integer NOT NULL,
    id_tag_object integer NOT NULL,
    id_application integer NOT NULL,
    id_role integer NOT NULL
);
COMMENT ON TABLE cor_app_privileges IS 'Cette table centrale, permet de gérer les droits d''usage des données en fonction du profil de l''utilisateur. Elle établi une correspondance entre l''affectation de tags génériques du schéma utilisateurs à un role pour une application avec les droits d''usage  (CREATE, READ, UPDATE, VALID, EXPORT, DELETE) et le type des données GeoNature (MY DATA, MY ORGANISM DATA, ALL DATA)';

----------------
--PRIMARY KEYS--
----------------

ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_pkey PRIMARY KEY (id_role, id_tag, id_application);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_roles ADD CONSTRAINT cor_roles_pkey PRIMARY KEY (id_role_groupe, id_role_utilisateur);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY bib_organismes ADD CONSTRAINT pk_bib_organismes PRIMARY KEY (id_organisme);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY bib_unites ADD CONSTRAINT pk_bib_services PRIMARY KEY (id_unite);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY t_roles ADD CONSTRAINT pk_roles PRIMARY KEY (id_role);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY t_applications ADD CONSTRAINT t_applications_pkey PRIMARY KEY (id_application);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY t_tags ADD CONSTRAINT pk_t_tags PRIMARY KEY (id_tag);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY bib_tag_types ADD CONSTRAINT pk_bib_tag_types PRIMARY KEY (id_tag_type);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_tags_relations ADD CONSTRAINT pk_cor_tags_relations PRIMARY KEY (id_tag_l, id_tag_r);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_organism_tag ADD CONSTRAINT pk_cor_organism_tag PRIMARY KEY (id_organism, id_tag);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_role_tag ADD CONSTRAINT pk_cor_role_tag PRIMARY KEY (id_role, id_tag);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_application_tag ADD CONSTRAINT pk_cor_application_tag PRIMARY KEY (id_application, id_tag);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT pk_cor_app_privileges PRIMARY KEY (id_tag_object, id_tag_action, id_application, id_role);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there

------------
--TRIGGERS--
------------

CREATE TRIGGER tri_modify_date_insert_t_roles BEFORE INSERT ON t_roles FOR EACH ROW EXECUTE PROCEDURE modify_date_insert();
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

CREATE TRIGGER tri_modify_date_update_t_roles BEFORE UPDATE ON t_roles FOR EACH ROW EXECUTE PROCEDURE modify_date_update();
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

CREATE TRIGGER tri_modify_date_insert_t_tags BEFORE INSERT ON t_tags FOR EACH ROW EXECUTE PROCEDURE modify_date_insert();
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

CREATE TRIGGER tri_modify_date_update_t_tags BEFORE UPDATE ON t_tags FOR EACH ROW EXECUTE PROCEDURE modify_date_update();
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

----------------
--FOREIGN KEYS--
----------------

ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_application_fkey FOREIGN KEY (id_application) REFERENCES utilisateurs.t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_tag_fkey FOREIGN KEY (id_tag) REFERENCES utilisateurs.t_tags(id_tag) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_role_fkey FOREIGN KEY (id_role) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_roles ADD CONSTRAINT cor_roles_id_role_groupe_fkey FOREIGN KEY (id_role_groupe) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY cor_roles ADD CONSTRAINT cor_roles_id_role_utilisateur_fkey FOREIGN KEY (id_role_utilisateur) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY t_roles ADD CONSTRAINT t_roles_id_organisme_fkey FOREIGN KEY (id_organisme) REFERENCES bib_organismes(id_organisme) ON UPDATE CASCADE;
ALTER TABLE ONLY t_roles ADD CONSTRAINT t_roles_id_unite_fkey FOREIGN KEY (id_unite) REFERENCES bib_unites(id_unite) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY bib_organismes ADD CONSTRAINT fk_bib_organismes_id_parent FOREIGN KEY (id_parent) REFERENCES bib_organismes(id_organisme) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY t_applications ADD CONSTRAINT fk_t_applications_id_parent FOREIGN KEY (id_parent) REFERENCES t_applications(id_application) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY t_tags ADD CONSTRAINT fk_t_tags_id_tag_type FOREIGN KEY (id_tag_type) REFERENCES bib_tag_types(id_tag_type) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_tags_relations ADD CONSTRAINT fk_cor_tags_relations_id_tag_l FOREIGN KEY (id_tag_l) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_tags_relations ADD CONSTRAINT fk_cor_tags_relations_id_tag_r FOREIGN KEY (id_tag_r) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_organism_tag ADD CONSTRAINT fk_cor_organism_tag_id_organism FOREIGN KEY (id_organism) REFERENCES bib_organismes(id_organisme) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_organism_tag ADD CONSTRAINT fk_cor_organism_tag_id_tag FOREIGN KEY (id_tag) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_role_tag ADD CONSTRAINT fk_cor_role_tag_id_role FOREIGN KEY (id_role) REFERENCES t_roles(id_role) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_role_tag ADD CONSTRAINT fk_cor_role_tag_id_tag FOREIGN KEY (id_tag) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_application_tag ADD CONSTRAINT fk_cor_application_tag_t_applications_id_application FOREIGN KEY (id_application) REFERENCES t_applications(id_application) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_application_tag ADD CONSTRAINT fk_cor_application_tag_t_tags_id_tag FOREIGN KEY (id_tag) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT fk_cor_app_privileges_id_tag_object FOREIGN KEY (id_tag_object) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT fk_cor_app_privileges_id_tag_action FOREIGN KEY (id_tag_action) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT fk_cor_app_privileges_id_application FOREIGN KEY (id_application) REFERENCES t_applications(id_application) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT fk_cor_app_privileges_id_role FOREIGN KEY (id_role) REFERENCES t_roles(id_role) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there

---------
--VIEWS--
---------

CREATE OR REPLACE VIEW utilisateurs.t_menus AS 
SELECT 
 t.id_tag AS id_menu,
 t.tag_name AS nom_menu,
 t.tag_desc AS desc_menu,
 c.id_application
FROM utilisateurs.bib_tag_types b
LEFT JOIN utilisateurs.t_tags t ON b.id_tag_type = t.id_tag_type
LEFT JOIN utilisateurs.cor_application_tag c ON c.id_tag = t.id_tag
WHERE b.id_tag_type = 4;

CREATE OR REPLACE VIEW utilisateurs.cor_role_menu AS 
SELECT 
DISTINCT
c.id_role,
c.id_tag AS id_menu
FROM utilisateurs.cor_role_tag c
JOIN utilisateurs.t_menus v ON v.id_menu = c.id_tag;		 

CREATE OR REPLACE VIEW utilisateurs.bib_droits AS 
SELECT 
 t.id_tag AS id_droit,
 t.tag_name AS nom_droit,
 t.tag_desc AS desc_droit
FROM utilisateurs.bib_tag_types b
JOIN utilisateurs.t_tags t ON b.id_tag_type = t.id_tag_type
WHERE b.id_tag_type = 3;	 

CREATE OR REPLACE VIEW utilisateurs.cor_role_droit_application AS 
SELECT 
 c.id_role,
 c.id_tag as id_droit, 
 c.id_application
FROM utilisateurs.cor_role_tag_application c; 

CREATE OR REPLACE VIEW v_userslist_forall_menu AS
 SELECT a.groupe,
    a.id_role,
    a.uuid_role,
    a.identifiant,
    a.nom_role,
    a.prenom_role,
    (upper(a.nom_role::text) || ' '::text) || a.prenom_role::text AS nom_complet,
    a.desc_role,
    a.pass,
    a.pass_plus,
    a.email,
    a.id_organisme,
    a.organisme,
    a.id_unite,
    a.remarques,
    a.pn,
    a.session_appli,
    a.date_insert,
    a.date_update,
    a.id_menu
   FROM ( SELECT u.groupe,
            u.id_role,
            u.uuid_role,
            u.identifiant,
            u.nom_role,
            u.prenom_role,
            u.desc_role,
            u.pass,
            u.pass_plus,
            u.email,
            u.id_organisme,
            u.organisme,
            u.id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_menu
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_role_menu c ON c.id_role = u.id_role
          WHERE u.groupe = false
        UNION
         SELECT u.groupe,
            u.id_role,
            u.uuid_role,
            u.identifiant,
            u.nom_role,
            u.prenom_role,
            u.desc_role,
            u.pass,
            u.pass_plus,
            u.email,
            u.id_organisme,
            u.organisme,
            u.id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_menu
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role
             JOIN utilisateurs.cor_role_menu c ON c.id_role = g.id_role_groupe
          WHERE u.groupe = false) a;
    EXCEPTION WHEN duplicate_object  THEN
    -- do nothing, it's already there

CREATE OR REPLACE VIEW v_userslist_forall_applications AS 
 SELECT a.groupe,
    a.id_role,
    a.identifiant,
    a.nom_role,
    a.prenom_role,
    a.desc_role,
    a.pass,
    a.pass_plus,
    a.email,
    a.id_organisme,
    a.organisme,
    a.id_unite,
    a.remarques,
    a.pn,
    a.session_appli,
    a.date_insert,
    a.date_update,
    max(a.id_droit) AS id_droit_max,
    a.id_application
   FROM ( SELECT u.groupe,
            u.id_role,
            u.identifiant,
            u.nom_role,
            u.prenom_role,
            u.desc_role,
            u.pass,
            u.pass_plus,
            u.email,
            u.id_organisme,
            u.organisme,
            u.id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_droit,
            c.id_application
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_role_droit_application c ON c.id_role = u.id_role
          WHERE u.groupe = false
        UNION
         SELECT u.groupe,
            u.id_role,
            u.identifiant,
            u.nom_role,
            u.prenom_role,
            u.desc_role,
            u.pass,
            u.pass_plus,
            u.email,
            u.id_organisme,
            u.organisme,
            u.id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_droit,
            c.id_application
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role
             JOIN utilisateurs.cor_role_droit_application c ON c.id_role = g.id_role_groupe
          WHERE u.groupe = false) a
  GROUP BY a.groupe, a.id_role, a.identifiant, a.nom_role, a.prenom_role, a.desc_role, a.pass, a.pass_plus, a.email, a.id_organisme, a.organisme, a.id_unite, a.remarques, a.pn, a.session_appli, a.date_insert, a.date_update, a.id_application;
  EXCEPTION WHEN duplicate_object  THEN
    -- do nothing, it's already there

CREATE OR REPLACE VIEW utilisateurs.v_usersaction_forall_gn_modules AS 
 WITH p_user_tag AS (
         SELECT u.id_role,
            u.identifiant,
            u.nom_role,
            u.prenom_role,
            u.desc_role,
            u.pass,
            u.pass_plus,
            u.email,
            u.id_organisme,
            c_1.id_tag_action,
            c_1.id_tag_object,
            c_1.id_application
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_app_privileges c_1 ON c_1.id_role = u.id_role
          WHERE u.groupe = false
        ), p_groupe_tag AS (
         SELECT u.id_role,
            u.identifiant,
            u.nom_role,
            u.prenom_role,
            u.desc_role,
            u.pass,
            u.pass_plus,
            u.email,
            u.id_organisme,
            c_1.id_tag_action,
            c_1.id_tag_object,
            c_1.id_application
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role OR g.id_role_groupe=u.id_role
             JOIN utilisateurs.cor_app_privileges c_1 ON c_1.id_role = g.id_role_groupe
          WHERE (g.id_role_groupe IN ( SELECT DISTINCT cor_roles.id_role_groupe
                   FROM utilisateurs.cor_roles))
        ), all_users_tags AS (
         SELECT v_1.id_role,
            v_1.identifiant,
            v_1.nom_role,
            v_1.prenom_role,
            v_1.desc_role,
            v_1.pass,
            v_1.pass_plus,
            v_1.email,
            v_1.id_organisme,
            v_1.id_application,
            v_1.id_tag_action,
            v_1.id_tag_object,
            t1.tag_code AS tag_action_code,
            t2.tag_code AS tag_object_code,
            max(t2.tag_code::text) OVER (PARTITION BY v_1.id_role, v_1.id_application, t1.tag_code) AS max_tag_object_code
           FROM ( SELECT a1.id_role,
                    a1.identifiant,
                    a1.nom_role,
                    a1.prenom_role,
                    a1.desc_role,
                    a1.pass,
                    a1.pass_plus,
                    a1.email,
                    a1.id_organisme,
                    a1.id_tag_action,
                    a1.id_tag_object,
                    a1.id_application
                   FROM p_user_tag a1
                UNION
                 SELECT a2.id_role,
                    a2.identifiant,
                    a2.nom_role,
                    a2.prenom_role,
                    a2.desc_role,
                    a2.pass,
                    a2.pass_plus,
                    a2.email,
                    a2.id_organisme,
                    a2.id_tag_action,
                    a2.id_tag_object,
                    a2.id_application
                   FROM p_groupe_tag a2) v_1
             JOIN utilisateurs.t_tags t1 ON t1.id_tag = v_1.id_tag_action
             JOIN utilisateurs.t_tags t2 ON t2.id_tag = v_1.id_tag_object
        )
 SELECT v.id_role,
    v.identifiant,
    v.nom_role,
    v.prenom_role,
    v.desc_role,
    v.pass,
    v.pass_plus,
    v.email,
    v.id_organisme,
    v.id_application,
    v.id_tag_action,
    v.id_tag_object,
    v.tag_action_code,
    v.max_tag_object_code::character varying(25) AS tag_object_code
   FROM all_users_tags v
  WHERE v.max_tag_object_code = v.tag_object_code::text;
EXCEPTION WHEN duplicate_object  THEN
    -- do nothing, it's already there
			 
-------------
--FUNCTIONS--
-------------

--With action id
CREATE OR REPLACE FUNCTION can_user_do_in_module(
    myuser integer,
    mymodule integer,
    myaction integer,
    mydataextend integer)
  RETURNS boolean AS
$BODY$
-- the function say if the given user can do the requested action in the requested module on the resquested data
-- USAGE : SELECT utilisateurs.can_user_do_in_module(requested_userid,requested_actionid,requested_moduleid,requested_dataextendid);
-- SAMPLE :SELECT utilisateurs.can_user_do_in_module(2,15,14,22);
  BEGIN
    IF myaction IN (SELECT id_tag_action FROM utilisateurs.v_usersaction_forall_gn_modules WHERE id_role = myuser AND id_application = mymodule AND id_tag_object >= mydataextend) THEN
      RETURN true;
    END IF;
    RETURN false;
  END;
$BODY$
  LANGUAGE plpgsql IMMUTABLE
  COST 100;

--With action code
CREATE OR REPLACE FUNCTION can_user_do_in_module(
    myuser integer,
    mymodule integer,
    myaction character varying,
    mydataextend integer)
  RETURNS boolean AS
$BODY$
-- the function say if the given user can do the requested action in the requested module on the resquested data
-- USAGE : SELECT utilisateurs.can_user_do_in_module(requested_userid,requested_actioncode,requested_moduleid,requested_dataextendid);
-- SAMPLE :SELECT utilisateurs.can_user_do_in_module(2,15,14,22);
  BEGIN
    IF myaction IN (SELECT tag_action_code FROM utilisateurs.v_usersaction_forall_gn_modules WHERE id_role = myuser AND id_application = mymodule AND id_tag_object >= mydataextend) THEN
      RETURN true;
    END IF;
    RETURN false;
  END;
$BODY$
  LANGUAGE plpgsql IMMUTABLE
  COST 100;

--With action id
CREATE OR REPLACE FUNCTION user_max_accessible_data_level_in_module(
    myuser integer,
    myaction integer,
    mymodule integer)
  RETURNS integer AS
$BODY$
DECLARE
  themaxleveldatatype integer;
-- the function return the max accessible extend of data the given user can access in the requested module
-- USAGE : SELECT utilisateurs.user_max_accessible_data_level_in_module(requested_userid,requested_actionid,requested_moduleid);
-- SAMPLE :SELECT utilisateurs.user_max_accessible_data_level_in_module(2,14,14);
  BEGIN
  SELECT max(tag_object_code::int) INTO themaxleveldatatype FROM utilisateurs.v_usersaction_forall_gn_modules WHERE id_role = myuser AND id_application = mymodule AND id_tag_action = myaction;
  RETURN themaxleveldatatype;
  END;
$BODY$
  LANGUAGE plpgsql IMMUTABLE
  COST 100;

--With action code
CREATE OR REPLACE FUNCTION user_max_accessible_data_level_in_module(
    myuser integer,
    myaction character varying,
    mymodule integer)
  RETURNS integer AS
$BODY$
DECLARE
  themaxleveldatatype integer;
-- the function return the max accessible extend of data the given user can access in the requested module
-- USAGE : SELECT utilisateurs.user_max_accessible_data_level_in_module(requested_userid,requested_actioncode,requested_moduleid);
-- SAMPLE :SELECT utilisateurs.user_max_accessible_data_level_in_module(2,14,14);
  BEGIN
  SELECT max(tag_object_code::int) INTO themaxleveldatatype FROM utilisateurs.v_usersaction_forall_gn_modules WHERE id_role = myuser AND id_application = mymodule AND tag_action_code = myaction;
  RETURN themaxleveldatatype;
  END;
$BODY$
  LANGUAGE plpgsql IMMUTABLE
  COST 100;

CREATE OR REPLACE FUNCTION find_all_modules_childs(myidapplication integer)
  RETURNS SETOF integer AS
$BODY$
 --Param : id_application d'un module ou d'une application quelque soit son rang
 --Retourne le id_application de tous les modules enfants + le module lui-même sous forme d'un jeu de données utilisable comme une table
 --Usage SELECT utilisateurs.find_all_modules_childs(14);
 --ou SELECT * FROM utilisateurs.t_applications WHERE id_application IN(SELECT * FROM utilisateurs.find_all_modules_childs(14))
  DECLARE
    inf RECORD;
    c integer;
  BEGIN
    SELECT INTO c count(*) FROM utilisateurs.t_applications WHERE id_parent = myidapplication;
    IF c > 0 THEN
      FOR inf IN
          WITH RECURSIVE modules AS (
          SELECT a1.id_application FROM utilisateurs.t_applications a1 WHERE a1.id_application = myidapplication
          UNION ALL
          SELECT a2.id_application FROM modules m JOIN utilisateurs.t_applications a2 ON a2.id_parent = m.id_application
    )
          SELECT id_application FROM modules
  LOOP
      RETURN NEXT inf.id_application;
  END LOOP;
    END IF;
  END;
$BODY$
  LANGUAGE plpgsql IMMUTABLE
  COST 100
  ROWS 1000;

CREATE OR REPLACE FUNCTION cruved_for_user_in_module(
    myuser integer,
    mymodule integer
  )
  RETURNS json AS
$BODY$
-- the function return user's CRUVED in the requested module
-- USAGE : SELECT utilisateurs.cruved_for_user_in_module(requested_userid,requested_moduleid);
-- SAMPLE :SELECT utilisateurs.cruved_for_user_in_module(2,14);
DECLARE
  thecruved json;
  BEGIN
	SELECT array_to_json(array_agg(row)) INTO thecruved
	FROM  (
	SELECT tag_action_code AS action, max(tag_object_code) AS level
	FROM utilisateurs.v_usersaction_forall_gn_modules
	WHERE id_role = myuser AND id_application = mymodule
	GROUP BY tag_action_code) row;
    RETURN thecruved;
  END;
$BODY$
  LANGUAGE plpgsql IMMUTABLE
  COST 100;
