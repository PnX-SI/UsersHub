-- Ce script permet de mettre à jour la structure et le contenu du schéma "utilisateurs" de UsersHub
-- et de recréer des vues qui simulent les tables de UsersHub V1
-- pour que les anciennes applications continuent à fonctionner

CREATE SCHEMA save;

-----------------------
--Compléter le schéma--
-----------------------

-- Creation des nouvelles tables

CREATE TABLE  IF NOT EXISTS utilisateurs.t_listes
(
  id_liste serial NOT NULL,
  code_liste character varying(20) NOT NULL,
  nom_liste character varying(50) NOT NULL,
  desc_liste text
);
COMMENT ON TABLE utilisateurs.t_listes IS 'Table des listes déroulantes des applications. Les roles de niveau groupes ou utilisateurs devant figurer dans une liste sont gérés dans la table cor_role_liste.';

CREATE TABLE IF NOT EXISTS utilisateurs.t_profils (
    id_profil serial NOT NULL,
    code_profil character varying(20),
    nom_profil character varying(255),
    desc_profil text
);
COMMENT ON TABLE utilisateurs.t_profils IS 'Table des profils d''utilisateurs génériques ou applicatifs, qui seront ensuite attachés à des roles et des applications.';

CREATE TABLE IF NOT EXISTS utilisateurs.cor_role_liste (
    id_role integer NOT NULL,
    id_liste integer NOT NULL
);
COMMENT ON TABLE utilisateurs.cor_role_liste IS 'Equivalent de l''ancienne cor_role_menu. Permet de créer des listes de roles (observateurs par ex.), sans notion de permission.';

CREATE TABLE IF NOT EXISTS utilisateurs.cor_profil_for_app (
    id_profil integer NOT NULL,
    id_application integer NOT NULL
);
COMMENT ON TABLE utilisateurs.cor_profil_for_app IS 'Permet d''attribuer et limiter les profils disponibles pour chacune des applications';

CREATE TABLE IF NOT EXISTS utilisateurs.cor_role_app_profil (
    id_role integer NOT NULL,
    id_application integer NOT NULL,
    id_profil integer NOT NULL
);
COMMENT ON TABLE utilisateurs.cor_role_app_profil IS 'Cette table centrale, permet d''associer des roles à des profils par application.';

-- Ajout des contraintes

ALTER TABLE ONLY utilisateurs.t_listes ADD CONSTRAINT pk_t_listes PRIMARY KEY (id_liste);
ALTER TABLE ONLY utilisateurs.t_profils ADD CONSTRAINT pk_t_profils PRIMARY KEY (id_profil);
ALTER TABLE ONLY utilisateurs.cor_role_liste ADD CONSTRAINT pk_cor_role_liste PRIMARY KEY (id_liste, id_role);
ALTER TABLE ONLY utilisateurs.cor_profil_for_app ADD CONSTRAINT pk_cor_profil_for_app PRIMARY KEY (id_application, id_profil);
ALTER TABLE ONLY utilisateurs.cor_role_app_profil ADD CONSTRAINT pk_cor_role_app_profil PRIMARY KEY (id_role, id_application, id_profil);

ALTER TABLE ONLY utilisateurs.cor_role_liste ADD CONSTRAINT fk_cor_role_liste_id_liste FOREIGN KEY (id_liste) REFERENCES utilisateurs.t_listes(id_liste) ON UPDATE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_liste ADD CONSTRAINT fk_cor_role_liste_id_role FOREIGN KEY (id_role) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_profil_for_app ADD CONSTRAINT fk_cor_profil_for_app_id_application FOREIGN KEY (id_application) REFERENCES utilisateurs.t_applications(id_application) ON UPDATE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_profil_for_app ADD CONSTRAINT fk_cor_profil_for_app_id_profil FOREIGN KEY (id_profil) REFERENCES utilisateurs.t_profils(id_profil) ON UPDATE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_app_profil ADD CONSTRAINT fk_cor_role_app_profil_id_role FOREIGN KEY (id_role) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_app_profil ADD CONSTRAINT fk_cor_role_app_profil_id_application FOREIGN KEY (id_application) REFERENCES utilisateurs.t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_app_profil ADD CONSTRAINT fk_cor_role_app_profil_id_profil FOREIGN KEY (id_profil) REFERENCES utilisateurs.t_profils(id_profil) ON UPDATE CASCADE ON DELETE CASCADE;


---------
--USERS--
---------
ALTER TABLE utilisateurs.t_roles ADD COLUMN active boolean;
ALTER TABLE utilisateurs.t_roles ALTER COLUMN active SET DEFAULT true;
UPDATE utilisateurs.t_roles SET active = true;


--------------
--ORGANISMES--
--------------
-- Creation d'un organisme générique s'il n'est pas deja dans la BDD
DO
$$
BEGIN
INSERT INTO utilisateurs.bib_organismes(uuid_organisme, nom_organisme, adresse_organisme, id_organisme) VALUES
('fd3c2619-0505-4a75-97e7-8cc37d096247', 'ALL', 'Représente tous les organismes', 0);
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;
-- Ajout de 2 champs url pour l'organisme et son logo
ALTER TABLE utilisateurs.bib_organismes ADD COLUMN url_organisme character varying(255);
ALTER TABLE utilisateurs.bib_organismes ADD COLUMN url_logo character varying(255);

----------------
--APPLICATIONS--
----------------

ALTER TABLE utilisateurs.t_applications ADD COLUMN code_application character varying(20);

UPDATE utilisateurs.t_applications SET code_application = id_application::character varying;
UPDATE utilisateurs.t_applications SET code_application = 'UH' WHERE nom_application ilike 'usershub' OR nom_application ilike 'application utilisateurs';
UPDATE utilisateurs.t_applications SET code_application = 'TH' WHERE nom_application ilike 'taxhub';
UPDATE utilisateurs.t_applications SET code_application = 'GN' WHERE nom_application ilike 'geonature' OR nom_application ilike 'application geonature';

ALTER TABLE utilisateurs.t_applications ALTER COLUMN code_application SET NOT NULL;

---------
--MENUS--
---------

-- Basculer les anciennes tables dans le schema "save"
ALTER TABLE utilisateurs.cor_role_menu SET SCHEMA save;
ALTER TABLE utilisateurs.t_menus SET SCHEMA save;
ALTER TABLE utilisateurs.cor_role_tag SET SCHEMA save;

--Récupérer les informations concernant les menus pour les mettre dans t_listes
DO
$$
BEGIN
INSERT INTO utilisateurs.t_listes (id_liste, code_liste, nom_liste, desc_liste)
SELECT id_menu, id_menu::character varying, nom_menu, desc_menu
FROM save.t_menus;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

DO
$$
BEGIN
INSERT INTO utilisateurs.t_listes (code_liste, nom_liste, desc_liste)
VALUES('obsocctax','Observateurs Occtax','Liste des observateurs du module Occtax');
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;
SELECT setval('utilisateurs.t_listes_id_liste_seq', (SELECT max(id_liste)+1 FROM utilisateurs.t_listes), false);
--TODO : récupérer la liste des observateurs occtax

--Récupérer les informations associant menu et utilisateurs
DO
$$
BEGIN
INSERT INTO utilisateurs.cor_role_liste (id_role, id_liste)
SELECT id_role, id_menu
FROM save.cor_role_menu;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


-- Vue recréant l'equivalent de t_menus
CREATE OR REPLACE VIEW utilisateurs.t_menus AS 
SELECT 
 id_liste AS id_menu,
 nom_liste AS nom_menu,
 desc_liste AS desc_menu,
 null::integer AS id_application
FROM utilisateurs.t_listes
;

-- Vue recréant l'equivalent de cor_role_menu
CREATE OR REPLACE VIEW cor_role_menu AS 
SELECT 
DISTINCT
crl.id_role,
crl.id_liste AS id_menu
FROM utilisateurs.cor_role_liste crl;


----------
--DROITS--
----------

-- Basculer les anciennes tables dans le schema "save"
ALTER TABLE utilisateurs.bib_droits SET SCHEMA save;
ALTER TABLE utilisateurs.cor_role_droit_application SET SCHEMA save;

DO
$$
BEGIN
INSERT INTO utilisateurs.t_profils (id_profil, code_profil, nom_profil, desc_profil)
SELECT id_droit, id_droit::character varying, nom_droit, desc_droit
FROM save.bib_droits;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;
SELECT setval('utilisateurs.t_profils_id_profil_seq', (SELECT max(id_profil)+1 FROM utilisateurs.t_profils), false);

UPDATE utilisateurs.t_profils 
SET nom_profil = 'Lecteur' 
,desc_profil = 'Ne peut que consulter/ou acceder' 
WHERE code_profil = '1';

DO
$$
BEGIN
INSERT INTO utilisateurs.cor_role_app_profil (id_role, id_application, id_profil)
SELECT id_role, id_application, id_droit
FROM save.cor_role_droit_application;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;




-- Association des profils aux applications
INSERT INTO utilisateurs.cor_profil_for_app (id_profil, id_application) VALUES
(6, (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'UH'))
,(2, (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'TH'))
,(3, (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'TH'))
,(4, (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'TH'))
,(6, (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'TH'))
,(1, (SELECT id_application FROM utilisateurs.t_applications WHERE code_application = 'GN'))
;
--Cette table doit être complétée pour les applications spécifiques de votre structure

---------
--VIEWS--
---------

-- Vue permettant de simuler le contenu de la table "t_menus" de la V1
CREATE OR REPLACE VIEW utilisateurs.t_menus AS 
SELECT 
 id_liste AS id_menu,
 nom_liste AS nom_menu,
 desc_liste AS desc_menu,
 null::integer AS id_application
FROM utilisateurs.t_listes
;

-- Vue permettant de simuler le contenu de la table "cor_role_menu" de la V1
CREATE OR REPLACE VIEW utilisateurs.cor_role_menu AS 
SELECT DISTINCT
crl.id_role,
crl.id_liste AS id_menu
FROM utilisateurs.cor_role_liste crl
JOIN utilisateurs.t_roles r ON r.id_role = crl.id_role AND r.active = true;	 

-- Vue permettant de simuler le contenu de la table "bib_droits" de la V1
CREATE OR REPLACE VIEW utilisateurs.bib_droits AS 
SELECT 
 id_profil AS id_droit,
 nom_profil AS nom_droit,
 desc_profil AS desc_droit
FROM utilisateurs.t_profils
WHERE id_profil <= 6;	 

-- Vue permettant de simuler le contenu de la table "cor_role_droit_application" de la V1
CREATE OR REPLACE VIEW utilisateurs.cor_role_droit_application AS 
SELECT 
 crap.id_role,
 crap.id_profil as id_droit, 
 crap.id_application
FROM utilisateurs.cor_role_app_profil crap
JOIN utilisateurs.t_roles r ON r.id_role = crap.id_role AND r.active = true; 

-- Vue permettant de retourner les utilisateurs des listes (menus)
DROP VIEW utilisateurs.v_userslist_forall_menu;
CREATE OR REPLACE VIEW utilisateurs.v_userslist_forall_menu AS
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
            o.nom_organisme AS organisme,
            0 AS id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_liste AS id_menu
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_role_liste c ON c.id_role = u.id_role
             LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
          WHERE u.groupe = false AND u.active = true
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
            o.nom_organisme AS organisme,
            0 AS id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_liste AS id_menu
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role
             JOIN utilisateurs.cor_role_liste c ON c.id_role = g.id_role_groupe
             LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
          WHERE u.groupe = false AND u.active = true) a;

-- Vue permettant de retourner les roles et leurs droits maximum pour chaque application
CREATE OR REPLACE VIEW utilisateurs.v_roleslist_forall_applications AS 
SELECT a.groupe,
    a.active,
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
	    u.active,
            o.nom_organisme AS organisme,
            0 AS id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_profil AS id_droit,
            c.id_application
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_role_app_profil c ON c.id_role = u.id_role
             JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
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
            u.active,
            o.nom_organisme AS organisme,
            0 AS id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_profil AS id_droit,
            c.id_application
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role OR g.id_role_groupe = u.id_role
             JOIN utilisateurs.cor_role_app_profil c ON c.id_role = g.id_role_groupe
             LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
          ) a
  WHERE a.active = true
  GROUP BY a.groupe, a.active, a.id_role, a.identifiant, a.nom_role, a.prenom_role, a.desc_role, a.pass, a.pass_plus, a.email, a.id_organisme, a.organisme, a.id_unite, a.remarques, a.pn, a.session_appli, a.date_insert, a.date_update, a.id_application;

-- Vue permettant de retourner les utilisateurs (pas les roles) et leurs droits maximum pour chaque application
DROP VIEW utilisateurs.v_userslist_forall_applications;
CREATE OR REPLACE VIEW utilisateurs.v_userslist_forall_applications AS 
SELECT * FROM utilisateurs.v_roleslist_forall_applications
WHERE groupe = false;



--On essaie de recréer une vue qui n'existe pas dans toutes les bases
--Si elle n'existe pas une erreur est levée et la création ne se fait pas.
DO
$$
BEGIN
DROP VIEW utilisateurs.v_nomade_obs;
CREATE OR REPLACE VIEW utilisateurs.v_nomade_obs AS 
SELECT DISTINCT r.id_role AS codeobs, (r.nom_role::text || ' '::text) || r.prenom_role::text AS nomprenom
FROM utilisateurs.t_roles r
WHERE (r.id_role IN ( 
        SELECT DISTINCT cr.id_role_utilisateur
        FROM utilisateurs.cor_roles cr
        WHERE (cr.id_role_groupe IN ( 
                SELECT id_role
                FROM utilisateurs.cor_role_menu
                WHERE id_menu = 5)
              ) 
        AND cr.id_role_utilisateur <> 999
        ORDER BY cr.id_role_utilisateur)
) 
OR (r.id_role IN ( 
        SELECT crm.id_role
        FROM utilisateurs.cor_role_menu crm
        JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 5 AND r.groupe = false)
        )
ORDER BY (r.nom_role::text || ' '::text) || r.prenom_role::text, r.id_role;
EXCEPTION WHEN undefined_table  THEN
        RAISE NOTICE 'Cette vue n''existe pas';
END
$$;

--Vues mobile.
DO
$$
BEGIN
DROP VIEW utilisateurs.v_nomade_observateurs_all;
CREATE OR REPLACE VIEW utilisateurs.v_nomade_observateurs_all AS 
        (        ( SELECT DISTINCT r.id_role, r.nom_role, r.prenom_role, 'fauna'::text AS mode
                   FROM utilisateurs.t_roles r
                  WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
                           FROM utilisateurs.cor_roles cr
                          WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
                                   FROM utilisateurs.cor_role_menu crm
                                  WHERE crm.id_menu = 11))
                          ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
                           FROM utilisateurs.cor_role_menu crm
                      JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 11 AND r.groupe = false AND r.active = true))
                  ORDER BY r.nom_role, r.prenom_role, r.id_role)
        UNION 
                ( SELECT DISTINCT r.id_role, r.nom_role, r.prenom_role, 'flora'::text AS mode
                   FROM utilisateurs.t_roles r
                  WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
                           FROM utilisateurs.cor_roles cr
                          WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
                                   FROM utilisateurs.cor_role_menu crm
                                  WHERE crm.id_menu = 5))
                          ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
                           FROM utilisateurs.cor_role_menu crm
                      JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 5 AND r.groupe = false AND r.active = true))
                  ORDER BY r.nom_role, r.prenom_role, r.id_role))
UNION 
        ( SELECT DISTINCT r.id_role, r.nom_role, r.prenom_role, 'inv'::text AS mode
           FROM utilisateurs.t_roles r
          WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
                   FROM utilisateurs.cor_roles cr
                  WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
                           FROM utilisateurs.cor_role_menu crm
                          WHERE crm.id_menu = 11))
                  ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
                   FROM utilisateurs.cor_role_menu crm
              JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 11 AND r.groupe = false AND r.active = true))
          ORDER BY r.nom_role, r.prenom_role, r.id_role);
EXCEPTION WHEN undefined_table  THEN
        RAISE NOTICE 'Cette vue n''existe pas';
END
$$;


-------------
--NETTOYAGE--
-------------

DROP VIEW utilisateurs.v_usersaction_forall_gn_modules;

ALTER TABLE utilisateurs.cor_application_tag SET SCHEMA save;
ALTER TABLE utilisateurs.cor_organism_tag SET SCHEMA save;
ALTER TABLE utilisateurs.cor_tags_relations SET SCHEMA save;
ALTER TABLE utilisateurs.cor_app_privileges SET SCHEMA save;
ALTER TABLE utilisateurs.t_tags SET SCHEMA save;
ALTER TABLE utilisateurs.bib_tag_types SET SCHEMA save;

-- Supprimer la table bib_unites inutilisée
-- Supprimer la FK vers bib_unites dans t_roles
ALTER TABLE utilisateurs.t_roles DROP COLUMN id_unite RESTRICT;
-- Supprimer le champs organisme de t_roles (https://github.com/PnEcrins/UsersHub/issues/38)
ALTER TABLE utilisateurs.t_roles DROP COLUMN organisme RESTRICT;

ALTER TABLE utilisateurs.bib_unites SET SCHEMA save;

--Rupture des liens entre le schéma save et utilisateurs
ALTER TABLE save.cor_app_privileges DROP CONSTRAINT fk_cor_app_privileges_id_application;
ALTER TABLE save.cor_app_privileges DROP CONSTRAINT fk_cor_app_privileges_id_role;
ALTER TABLE save.cor_app_privileges DROP CONSTRAINT fk_cor_app_privileges_id_tag_action;
ALTER TABLE save.cor_app_privileges DROP CONSTRAINT fk_cor_app_privileges_id_tag_object;
ALTER TABLE save.cor_organism_tag DROP CONSTRAINT fk_cor_organism_tag_id_organism;
ALTER TABLE save.cor_organism_tag DROP CONSTRAINT fk_cor_organism_tag_id_tag;
ALTER TABLE save.cor_role_droit_application DROP CONSTRAINT cor_role_droit_application_id_application_fkey;
ALTER TABLE save.cor_role_droit_application DROP CONSTRAINT cor_role_droit_application_id_droit_fkey;
ALTER TABLE save.cor_role_droit_application DROP CONSTRAINT cor_role_droit_application_id_role_fkey;
ALTER TABLE save.cor_role_menu DROP CONSTRAINT cor_role_menu_application_id_menu_fkey;
ALTER TABLE save.cor_role_menu DROP CONSTRAINT cor_role_menu_application_id_role_fkey;
ALTER TABLE save.cor_role_tag DROP CONSTRAINT fk_cor_role_tag_id_role;
ALTER TABLE save.cor_role_tag DROP CONSTRAINT fk_cor_role_tag_id_tag;
ALTER TABLE save.cor_tags_relations DROP CONSTRAINT fk_cor_tags_relations_id_tag_l;
ALTER TABLE save.cor_tags_relations DROP CONSTRAINT fk_cor_tags_relations_id_tag_r;
ALTER TABLE save.t_menus DROP CONSTRAINT t_menus_id_application_fkey;
ALTER TABLE save.t_tags DROP CONSTRAINT fk_t_tags_id_tag_type;


DROP FUNCTION utilisateurs.can_user_do_in_module(integer, integer, integer, integer);
DROP FUNCTION utilisateurs.can_user_do_in_module(integer, integer, character varying, integer);
DROP FUNCTION utilisateurs.user_max_accessible_data_level_in_module(integer, integer, integer);
DROP FUNCTION utilisateurs.user_max_accessible_data_level_in_module(integer, character varying, integer);
DROP FUNCTION utilisateurs.find_all_modules_childs(integer);

--------
--SAVE--
--------
-------
--GN1--
-------
--TODO AVANT  SUPPRESSION : 
--recréer les vues de GN1
--  contactfaune.v_nomade_observateurs_faune
--  contactflore.v_nomade_observateurs_flore
--  contactinv.v_nomade_observateurs_inv
-- à compléter

-- DO
-- $$
-- BEGIN
-- DROP VIEW utilisateurs.v_observateurs;
-- CREATE OR REPLACE VIEW utilisateurs.v_observateurs AS 
--  SELECT DISTINCT r.id_role AS codeobs, (r.nom_role::text || ' '::text) || r.prenom_role::text AS nomprenom
--    FROM utilisateurs.t_roles r
--   WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
--            FROM utilisateurs.cor_roles cr
--           WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
--                    FROM utilisateurs.cor_role_menu crm
--                   WHERE crm.id_menu = 5))
--           ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
--            FROM utilisateurs.cor_role_menu crm
--       JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 5 AND r.groupe = false AND r.active = true))
--   ORDER BY (r.nom_role::text || ' '::text) || r.prenom_role::text, r.id_role;
--   EXCEPTION WHEN undefined_table  THEN
--         RAISE NOTICE 'Cet vue n''existe pas';
-- END
-- $$;

-- DO
-- $$
-- BEGIN
-- DROP VIEW contactfaune.v_nomade_observateurs_faune;
-- CREATE OR REPLACE VIEW contactfaune.v_nomade_observateurs_faune AS 
--  SELECT DISTINCT r.id_role, r.nom_role, r.prenom_role
--    FROM utilisateurs.t_roles r
--   WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
--            FROM utilisateurs.cor_roles cr
--           WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
--                    FROM utilisateurs.cor_role_menu crm
--                   WHERE crm.id_menu = 11))
--           ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
--            FROM utilisateurs.cor_role_menu crm
--       JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 11 AND r.groupe = false AND r.active = true))
--   ORDER BY r.nom_role, r.prenom_role, r.id_role;
-- EXCEPTION WHEN undefined_table  THEN
--         RAISE NOTICE 'Cet vue n''existe pas';
-- END
-- $$;

-- DO
-- $$
-- BEGIN
-- DROP VIEW contactinv.v_nomade_observateurs_inv;
-- CREATE OR REPLACE VIEW contactinv.v_nomade_observateurs_inv AS 
--  SELECT DISTINCT r.id_role, r.nom_role, r.prenom_role
--    FROM utilisateurs.t_roles r
--   WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
--            FROM utilisateurs.cor_roles cr
--           WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
--                    FROM utilisateurs.cor_role_menu crm
--                   WHERE crm.id_menu = 11))
--           ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
--            FROM utilisateurs.cor_role_menu crm
--       JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 11 AND r.groupe = false AND r.active = true))
--   ORDER BY r.nom_role, r.prenom_role, r.id_role;
--   EXCEPTION WHEN undefined_table  THEN
--         RAISE NOTICE 'Cet vue n''existe pas';
-- END
-- $$;



--Rechercher les vues qui doivent être réécrites car pointant sur les tables déplacées dans le schéma save
-- SELECT dependent_ns.nspname as dependent_schema
-- , dependent_view.relname as dependent_view 
-- , source_ns.nspname as source_schema
-- , source_table.relname as source_table
-- , pg_attribute.attname as column_name
-- FROM pg_depend 
-- JOIN pg_rewrite ON pg_depend.objid = pg_rewrite.oid 
-- JOIN pg_class as dependent_view ON pg_rewrite.ev_class = dependent_view.oid 
-- JOIN pg_class as source_table ON pg_depend.refobjid = source_table.oid 
-- JOIN pg_attribute ON pg_depend.refobjid = pg_attribute.attrelid 
--     AND pg_depend.refobjsubid = pg_attribute.attnum 
-- JOIN pg_namespace dependent_ns ON dependent_ns.oid = dependent_view.relnamespace
-- JOIN pg_namespace source_ns ON source_ns.oid = source_table.relnamespace
-- WHERE 
-- source_ns.nspname = 'save'
-- AND source_table.relname IN('cor_role_menu', 't_menus', 'bib_droits', 'cor_role_droit_application')
-- AND pg_attribute.attnum > 0 
-- --AND pg_attribute.attname = 'my_column'
-- ORDER BY 1,2;


--TABLES SUPPRIMABLES (dans cet ordre). A la discretion de chacun

--DROP TABLE save.cor_application_tag;
--DROP TABLE save.cor_organism_tag;
--DROP TABLE save.cor_tags_relations;
--DROP TABLE save.cor_role_menu;
--DROP TABLE save.t_menus;
--DROP TABLE save.cor_role_droit_application;
--DROP TABLE save.bib_droits;
--DROP TABLE save.bib_unites;

--Ces 3 tables sont utilisées depuis le script de migration de la base de données GéoNature
--Vous ne devez pas les supprimer avant d'avoir exécuté cette migration GéoNature.
--DROP TABLE save.cor_app_privileges;
--DROP TABLE save.t_tags;
--DROP TABLE save.bib_tag_types;
