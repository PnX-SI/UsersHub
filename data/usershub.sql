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

CREATE TABLE IF NOT EXISTS cor_role_menu (
    id_role integer NOT NULL,
    id_menu integer NOT NULL
);
COMMENT ON TABLE cor_role_menu IS 'gestion du contenu des menus utilisateurs dans les applications';

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
    organisme character(32),
    id_unite integer,
    remarques text,
    pn boolean,
    session_appli character varying(50),
    date_insert timestamp without time zone,
    date_update timestamp without time zone
);

DO
$$
BEGIN
CREATE SEQUENCE t_roles_id_role_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
END
$$;
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

DO
$$
BEGIN
CREATE SEQUENCE bib_organismes_id_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
END
$$;
ALTER SEQUENCE bib_organismes_id_seq OWNED BY bib_organismes.id_organisme;
ALTER TABLE ONLY bib_organismes ALTER COLUMN id_organisme SET DEFAULT nextval('bib_organismes_id_seq'::regclass);


CREATE TABLE IF NOT EXISTS bib_droits (
    id_droit integer NOT NULL,
    nom_droit character varying(50),
    desc_droit text
);


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


DO
$$
BEGIN
CREATE SEQUENCE bib_unites_id_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
END
$$;
ALTER SEQUENCE bib_unites_id_seq OWNED BY bib_unites.id_unite;
ALTER TABLE ONLY bib_unites ALTER COLUMN id_unite SET DEFAULT nextval('bib_unites_id_seq'::regclass);


CREATE TABLE IF NOT EXISTS cor_role_droit_application (
    id_role integer NOT NULL,
    id_droit integer NOT NULL,
    id_application integer NOT NULL
);


CREATE TABLE IF NOT EXISTS t_applications (
    id_application integer NOT NULL,
    nom_application character varying(50) NOT NULL,
    desc_application text,
    id_parent integer
);

DO
$$
BEGIN
CREATE SEQUENCE t_applications_id_application_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
END
$$;
ALTER SEQUENCE t_applications_id_application_seq OWNED BY t_applications.id_application;
ALTER TABLE ONLY t_applications ALTER COLUMN id_application SET DEFAULT nextval('t_applications_id_application_seq'::regclass);


CREATE TABLE IF NOT EXISTS t_menus (
    id_menu integer NOT NULL,
    nom_menu character varying(50) NOT NULL,
    desc_menu text,
    id_application integer
);
COMMENT ON TABLE t_menus IS 'table des menus déroulants des applications. Les roles de niveau groupes ou utilisateurs devant figurer dans un menu sont gérés dans la table cor_role_menu_application.';

DO
$$
BEGIN
CREATE SEQUENCE t_menus_id_menu_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
END
$$;
ALTER SEQUENCE t_menus_id_menu_seq OWNED BY t_menus.id_menu;
ALTER TABLE ONLY t_menus ALTER COLUMN id_menu SET DEFAULT nextval('t_menus_id_menu_seq'::regclass);


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

DO
$$
BEGIN
CREATE SEQUENCE t_tags_id_tag_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
EXCEPTION WHEN duplicate_table THEN
        -- do nothing, it's already there
END
$$;
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
DO
$$
BEGIN
ALTER TABLE ONLY bib_droits ADD CONSTRAINT bib_droits_pkey PRIMARY KEY (id_droit);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_role_droit_application ADD CONSTRAINT cor_role_droit_application_pkey PRIMARY KEY (id_role, id_droit, id_application);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_role_menu ADD CONSTRAINT cor_role_menu_pkey PRIMARY KEY (id_role, id_menu);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_roles ADD CONSTRAINT cor_roles_pkey PRIMARY KEY (id_role_groupe, id_role_utilisateur);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY bib_organismes ADD CONSTRAINT pk_bib_organismes PRIMARY KEY (id_organisme);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY bib_unites ADD CONSTRAINT pk_bib_services PRIMARY KEY (id_unite);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY t_roles ADD CONSTRAINT pk_roles PRIMARY KEY (id_role);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;


DO
$$
BEGIN
ALTER TABLE ONLY t_applications ADD CONSTRAINT t_applications_pkey PRIMARY KEY (id_application);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY t_menus ADD CONSTRAINT t_menus_pkey PRIMARY KEY (id_menu);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY t_tags ADD CONSTRAINT pk_t_tags PRIMARY KEY (id_tag);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY bib_tag_types ADD CONSTRAINT pk_bib_tag_types PRIMARY KEY (id_tag_type);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_tags_relations ADD CONSTRAINT pk_cor_tags_relations PRIMARY KEY (id_tag_l, id_tag_r);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_organism_tag ADD CONSTRAINT pk_cor_organism_tag PRIMARY KEY (id_organism, id_tag);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_role_tag ADD CONSTRAINT pk_cor_role_tag PRIMARY KEY (id_role, id_tag);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_application_tag ADD CONSTRAINT pk_cor_application_tag PRIMARY KEY (id_application, id_tag);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT pk_cor_app_privileges PRIMARY KEY (id_tag_object, id_tag_action, id_application, id_role);
EXCEPTION WHEN invalid_table_definition  THEN
        -- do nothing, it's already there
END
$$;


------------
--TRIGGERS--
------------
DO
$$
BEGIN
CREATE TRIGGER tri_modify_date_insert_t_roles BEFORE INSERT ON t_roles FOR EACH ROW EXECUTE PROCEDURE modify_date_insert();
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
CREATE TRIGGER tri_modify_date_update_t_roles BEFORE UPDATE ON t_roles FOR EACH ROW EXECUTE PROCEDURE modify_date_update();
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
CREATE TRIGGER tri_modify_date_insert_t_tags BEFORE INSERT ON t_tags FOR EACH ROW EXECUTE PROCEDURE modify_date_insert();
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
CREATE TRIGGER tri_modify_date_update_t_tags BEFORE UPDATE ON t_tags FOR EACH ROW EXECUTE PROCEDURE modify_date_update();
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;


----------------
--FOREIGN KEYS--
----------------
DO
$$
BEGIN
ALTER TABLE ONLY cor_role_droit_application ADD CONSTRAINT cor_role_droit_application_id_application_fkey FOREIGN KEY (id_application) REFERENCES t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY cor_role_droit_application ADD CONSTRAINT cor_role_droit_application_id_droit_fkey FOREIGN KEY (id_droit) REFERENCES bib_droits(id_droit) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY cor_role_droit_application ADD CONSTRAINT cor_role_droit_application_id_role_fkey FOREIGN KEY (id_role) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_role_menu ADD CONSTRAINT cor_role_menu_application_id_menu_fkey FOREIGN KEY (id_menu) REFERENCES t_menus(id_menu) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY cor_role_menu ADD CONSTRAINT cor_role_menu_application_id_role_fkey FOREIGN KEY (id_role) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_roles ADD CONSTRAINT cor_roles_id_role_groupe_fkey FOREIGN KEY (id_role_groupe) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY cor_roles ADD CONSTRAINT cor_roles_id_role_utilisateur_fkey FOREIGN KEY (id_role_utilisateur) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY t_menus
    ADD CONSTRAINT t_menus_id_application_fkey FOREIGN KEY (id_application) REFERENCES t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY t_roles ADD CONSTRAINT t_roles_id_organisme_fkey FOREIGN KEY (id_organisme) REFERENCES bib_organismes(id_organisme) ON UPDATE CASCADE;
ALTER TABLE ONLY t_roles ADD CONSTRAINT t_roles_id_unite_fkey FOREIGN KEY (id_unite) REFERENCES bib_unites(id_unite) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY bib_organismes ADD CONSTRAINT fk_bib_organismes_id_parent FOREIGN KEY (id_parent) REFERENCES bib_organismes(id_organisme) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY t_applications ADD CONSTRAINT fk_t_applications_id_parent FOREIGN KEY (id_parent) REFERENCES t_applications(id_application) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY t_tags ADD CONSTRAINT fk_t_tags_id_tag_type FOREIGN KEY (id_tag_type) REFERENCES bib_tag_types(id_tag_type) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_tags_relations ADD CONSTRAINT fk_cor_tags_relations_id_tag_l FOREIGN KEY (id_tag_l) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_tags_relations ADD CONSTRAINT fk_cor_tags_relations_id_tag_r FOREIGN KEY (id_tag_r) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_organism_tag ADD CONSTRAINT fk_cor_organism_tag_id_organism FOREIGN KEY (id_organism) REFERENCES bib_organismes(id_organisme) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_organism_tag ADD CONSTRAINT fk_cor_organism_tag_id_tag FOREIGN KEY (id_tag) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_role_tag ADD CONSTRAINT fk_cor_role_tag_id_role FOREIGN KEY (id_role) REFERENCES t_roles(id_role) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_role_tag ADD CONSTRAINT fk_cor_role_tag_id_tag FOREIGN KEY (id_tag) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_application_tag ADD CONSTRAINT fk_cor_application_tag_t_applications_id_application FOREIGN KEY (id_application) REFERENCES t_applications(id_application) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_application_tag ADD CONSTRAINT fk_cor_application_tag_t_tags_id_tag FOREIGN KEY (id_tag) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;

DO
$$
BEGIN
ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT fk_cor_app_privileges_id_tag_object FOREIGN KEY (id_tag_object) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT fk_cor_app_privileges_id_tag_action FOREIGN KEY (id_tag_action) REFERENCES t_tags(id_tag) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT fk_cor_app_privileges_id_application FOREIGN KEY (id_application) REFERENCES t_applications(id_application) ON UPDATE CASCADE;
ALTER TABLE ONLY cor_app_privileges ADD CONSTRAINT fk_cor_app_privileges_id_role FOREIGN KEY (id_role) REFERENCES t_roles(id_role) ON UPDATE CASCADE;
EXCEPTION WHEN duplicate_object  THEN
        -- do nothing, it's already there
END
$$;


---------
--VIEWS--
---------
DO
$$
BEGIN
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
END
$$;

DO
$$
BEGIN
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
END
$$;

DO
$$
BEGIN
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
             JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role
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
END
$$;


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


--------
--DATA--
--------
DO
$$
BEGIN
INSERT INTO bib_droits (id_droit, nom_droit, desc_droit) VALUES 
(5, 'validateur', 'Il valide bien sur')
,(4, 'modérateur', 'Peu utilisé')
,(0, 'aucun', 'aucun droit.')
,(1, 'utilisateur', 'Ne peut que consulter')
,(2, 'rédacteur', 'Il possède des droit d''écriture pour créer des enregistrements')
,(6, 'administrateur', 'Il a tous les droits')
,(3, 'référent', 'utilisateur ayant des droits complémentaires au rédacteur (par exemple exporter des données ou autre)')
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO bib_organismes (nom_organisme, adresse_organisme, cp_organisme, ville_organisme, tel_organisme, fax_organisme, email_organisme, id_organisme) VALUES 
('PNF', NULL, NULL, 'Montpellier', NULL, NULL, NULL, 1)
,('Parc National des Ecrins', 'Domaine de Charance', '05000', 'GAP', '04 92 40 20 10', '', '', 2)
,('Autre', '', '', '', '', '', '', -1)
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES 
('Virtuel', NULL, NULL, NULL, NULL, NULL, NULL, 1)
,('Personnels partis', NULL, NULL, NULL, NULL, NULL, NULL, 2)
,('Stagiaires', NULL, NULL, '', '', NULL, NULL, 3)
,('Secretariat général', '', '', '', '', NULL, NULL, 4)
,('Service scientifique', '', '', '', '', NULL, NULL, 5)
,('Service SI', '', '', '', '', NULL, NULL, 6)
,('Service Communication', '', '', '', '', NULL, NULL, 7)
,('Conseil scientifique', '', '', '', NULL, NULL, NULL, 8)
,('Conseil d''administration', '', '', '', NULL, NULL, NULL, 9)
,('Partenaire fournisseur', NULL, NULL, NULL, NULL, NULL, NULL, 10)
,('Autres', NULL, NULL, NULL, NULL, NULL, NULL, -1)
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO t_applications (id_application, nom_application, desc_application, id_parent) VALUES 
(1, 'application utilisateurs', 'application permettant d''administrer la présente base de données.',NULL)
,(2, 'taxhub', 'application permettant d''administrer la liste des taxons.',NULL)
,(14, 'application geonature', 'Application permettant la consultation et la gestion des relevés faune et flore.',NULL)
,(15, 'contact (GeoNature2)', 'Module contact faune-flore-fonge de GeoNature', 14)
;
PERFORM pg_catalog.setval('t_applications_id_application_seq', 15, true);
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, organisme, id_unite, pn, session_appli, date_insert, date_update, id_organisme, remarques) VALUES 
(true, 20001, NULL,   'grp_socle 2', NULL, 'Bureau d''étude socle 2', NULL, NULL, 'mastructure', -1, true, NULL, NULL, NULL, NULL, 'Groupe à droit étendu')
,(true, 20002, NULL, 'grp_en_poste', NULL, 'Tous les agents en poste au PN', NULL, NULL, 'mastructure', -1, true, NULL, NULL, NULL, NULL,'groupe test')
,(true, 20003, NULL, 'grp_socle 1', NULL, 'Bureau d''étude socle 1', NULL, NULL,'mastructure', -1, true, NULL, NULL, NULL, NULL,'Groupe à droit limité')
;
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, organisme, id_unite, pn, session_appli, date_insert, date_update, id_organisme, remarques, pass_plus) VALUES 
(false, 1, 'admin', 'Administrateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, 'Autre', -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier', '$2y$13$TMuRXgvIg6/aAez0lXLLFu0lyPk4m8N55NDhvLoUHh/Ar3rFzjFT.')
,(false, 2, 'agent', 'Agent', 'test', NULL, 'b33aed8f3134996703dc39f9a7c95783', NULL, 'Autre', -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false, 3, 'partenaire', 'Partenaire', 'test', NULL, '5bd40a8524882d75f3083903f2c912fc', NULL, 'Autre', -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false,4, 'pierre.paul', 'Paul', 'Pierre', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, 'Autre', -1, false, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false,5, 'validateur', 'validateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, 'Autre', -1, false, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN 
INSERT INTO cor_role_droit_application (id_role, id_droit, id_application) 
VALUES (1, 6, 1)
,(1, 6, 2)
,(1, 6, 14)
,(20002, 3, 14)
,(2, 2, 14)
,(3, 1, 14)
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN 
INSERT INTO t_menus (id_menu, nom_menu, desc_menu, id_application) 
VALUES (9, 'faune - Observateurs', 'Listes des observateurs faune', 14)
,(10, 'flore - Observateurs', 'Liste des observateurs flore', 14)
;
PERFORM pg_catalog.setval('t_menus_id_menu_seq', 11, true);
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO cor_role_menu (id_role, id_menu) VALUES 
(1, 10)
,(1, 9)
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO cor_roles (id_role_groupe, id_role_utilisateur) 
VALUES (20002, 1)
,(20002, 2)
,(20002, 4)
,(20002, 5)
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO bib_tag_types(id_tag_type, tag_type_name, tag_type_desc) VALUES
(1, 'Object', 'Define a type object. Usually to define privileges on an object.')
,(2, 'Action', 'Define a type action. Usually to define privileges for an action.')
,(3, 'Privilege', 'Define a privilege level.')
,(4, 'Liste', 'Define a type liste for grouping anything.')
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

DO
$$
BEGIN
INSERT INTO t_tags (id_tag, id_tag_type, tag_code, tag_name, tag_label, tag_desc) VALUES
(1, 3,'1','utilisateur', 'Utilisateur','Ne peut que consulter')
,(2, 3, '2', 'rédacteur', 'Rédacteur','Il possède des droit d''écriture pour créer des enregistrements')
,(3, 3, '3', 'référent', 'Référent','Utilisateur ayant des droits complémentaires au rédacteur (par exemple exporter des données ou autre)')
,(4, 3, '4', 'modérateur', 'Modérateur', 'Peu utilisé')
,(5, 3, '5', 'validateur', 'Validateur', 'Il valide bien sur')
,(6, 3, '6', 'administrateur', 'Administrateur', 'Il a tous les droits')
,(11, 2, 'C', 'create', 'Create', 'Can create/add new data')
,(12, 2, 'R', 'read', 'Read', 'Can read data')
,(13, 2, 'U', 'update', 'Update', 'Can update data')
,(14, 2, 'V', 'validate', 'Validate', 'Can validate data')
,(15, 2, 'E', 'export', 'Export', 'Can export data')
,(16, 2, 'D', 'delete', 'Delete', 'Can delete data')
,(20, 3, '0', 'nothing', 'Nothing', 'Cannot do anything')
,(21, 3, '1', 'my data', 'My data', 'Can do action only on my data')
,(22, 3, '2', 'my organism data', 'My organism data', 'Can do action only on my data and on my organism data')
,(23, 3, '3', 'all data', 'All data', 'Can do action on all data')

,(100, 4, NULL, 'observateurs flore', 'Observateurs flore','Liste des observateurs pour les protocoles flore')
,(101, 4, NULL, 'observateurs faune', 'Observateurs faune','Liste des observateurs pour les protocoles faune')
,(102, 4, NULL, 'observateurs aigle', 'Observateurs aigle', 'Liste des observateurs pour le protocole suivi de la reproduction de l''aigle royal')
;
PERFORM pg_catalog.setval('t_tags_id_tag_seq', 104, true);
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO cor_role_tag (id_role, id_tag) VALUES
--Liste des observateurs faune
(1,101)
,(20002,101)
,(5,101)
-- --Liste des observateurs flore
,(2,100)
,(5,100)
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


DO
$$
BEGIN
INSERT INTO cor_app_privileges (id_tag_action, id_tag_object, id_application, id_role) VALUES
--Administrateur sur UsersHub et TaxHub
(6,23,1,1)
,(6,23,2,1)
--Administrateur sur GeoNature
,(11, 23, 14, 1)
,(12, 23, 14, 1)
,(13, 23, 14, 1)
,(14, 23, 14, 1)
,(15, 23, 14, 1)
,(16, 23, 14, 1)
--Validateur général sur tout GeoNature
,(14, 23, 14, 5)
--Validateur pour son organisme sur contact
,(14, 22, 15, 4)
--CRUVED du groupe en poste sur tout GeoNature
,(11, 23, 14, 20002)
,(12, 22, 14, 20002)
,(13, 21, 14, 20002)
,(15, 22, 14, 20002)
,(16, 21, 14, 20002)
--Groupe bureau d''étude socle 2 sur tout GeoNature
,(11, 23, 14, 20001)
,(12, 22, 14, 20001)
,(13, 21, 14, 20001)
,(15, 22, 14, 20001)
,(16, 21, 14, 20001)
--Groupe bureau d''étude socle 1 sur tout GeoNature
,(11, 23, 14, 20003)
,(12, 21, 14, 20003)
,(13, 21, 14, 20003)
,(15, 21, 14, 20003)
,(16, 21, 14, 20003)
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;
