-- Ce script permet de recréer des tables qui simulent les tables de UsersHub V1
-- pour que les anciennes applications continuent à fonctionner

--TODO : test this script

CREATE SCHEMA save;


----------------
--APPLICATIONS--
----------------
--TODO : avant d'exécuter ce script, GeoNature et occtax + d'éventuels autres modules doivent être présents dans t_applications
INSERT INTO utilisateurs.cor_application_tag (id_tag, id_application)
SELECT t.id_tag, (SELECT id_application FROM utilisateurs.t_applications WHERE nom_application IN('occtax')) 
FROM utilisateurs.t_tags t
JOIN utilisateurs.t_menus  m ON m.nom_menu = t.tag_name
WHERE id_tag_type = 4
AND tag_name ILIKE 'observateurs occtax';


---------
--MENUS--
---------
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
VALUES('obsocctax','observateurs occtax','Liste des observateurs du module occtax');
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;
--TODO : récupérer la liste des observateurs occtax

--Récupérer les informations associant menu et utilisateurs
DO
$$
BEGIN
INSERT INTO utilisateurs.cor_role_liste (id_role, id_liste)
SELECT id_role, id_liste
FROM save.cor_role_menu;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

--cas particulier d'occtax qui n'a pas d'enregistrement dans t_menus de la v1
INSERT INTO utilisateurs.cor_role_liste (id_role, id_liste)
SELECT crt.id_role, (SELECT id_liste FROM utilisateurs.t_listes WHERE code_liste = 'obsocctax') AS id_liste 
FROM save.cor_role_tag crt
WHERE crt.id_tag = (SELECT id_tag FROM utilisateurs.t_tags WHERE tag_name ILIKE 'observateurs occtax');
--TODO pour chaque module comme occtax. A creuser

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

-- Vue recréant l'équivalent de bib_droits à partir des tags existants
CREATE OR REPLACE VIEW utilisateurs.bib_droits AS 
SELECT 
 id_profil AS id_droit,
 nom_profil AS nom_droit,
 desc_profil AS desc_droit
FROM utilisateurs.t_profils
WHERE id_profil <= 6;


-- Vue recréant l'équivalent de cor_role_droit_application
CREATE OR REPLACE VIEW utilisateurs.cor_role_droit_application AS 
SELECT 
 id_role,
 id_profil as id_droit, 
 id_application
FROM utilisateurs.cor_role_app_profil;

----------------
--APPLICATIONS--
----------------
ALTER TABLE utilisateurs.t_applications ADD COLUMN code_application character varying(20);
ALTER TABLE utilisateurs.t_applications ALTER COLUMN code_application SET NOT NULL;
UPDATE utilisateurs.t_applications SET code_application = id_application::character varying;
UPDATE utilisateurs.t_applications SET code_application = 'UH' WHERE nom_application ilike 'usershub' OR nom_application ilike 'application utilisateurs';
UPDATE utilisateurs.t_applications SET code_application = 'TH' WHERE nom_application ilike 'taxhub';
UPDATE utilisateurs.t_applications SET code_application = 'GN' WHERE nom_application ilike 'geonature';


----------
--AUTRES--
----------
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
            0 AS id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_liste AS id_menu
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_role_liste c ON c.id_role = u.id_role
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
          WHERE u.groupe = false) a;

-- Vue permettant de retourner les utilisateurs et leurs droits maximum pour chaque application
DROP VIEW utilisateurs.v_userslist_forall_applications;
CREATE OR REPLACE VIEW utilisateurs.v_userslist_forall_applications AS 
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
            0 AS id_unite,
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
            0 AS id_unite,
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
  GROUP BY a.groupe, a.id_role, a.identifiant, a.nom_role, a.prenom_role, a.desc_role, a.pass, a.pass_plus, a.email, a.id_organisme, a.id_unite, a.remarques, a.pn, a.session_appli, a.date_insert, a.date_update, a.id_application;

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
        RAISE NOTICE 'Cet vue n''existe pas';
END
$$;

--vues mobile.
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
                      JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 11 AND r.groupe = false))
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
                      JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 5 AND r.groupe = false))
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
              JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 11 AND r.groupe = false))
          ORDER BY r.nom_role, r.prenom_role, r.id_role);
EXCEPTION WHEN undefined_table  THEN
        RAISE NOTICE 'Cet vue n''existe pas';
END
$$;

DO
$$
BEGIN
DROP VIEW utilisateurs.v_observateurs;
CREATE OR REPLACE VIEW utilisateurs.v_observateurs AS 
 SELECT DISTINCT r.id_role AS codeobs, (r.nom_role::text || ' '::text) || r.prenom_role::text AS nomprenom
   FROM utilisateurs.t_roles r
  WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
           FROM utilisateurs.cor_roles cr
          WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
                   FROM utilisateurs.cor_role_menu crm
                  WHERE crm.id_menu = 5))
          ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
           FROM utilisateurs.cor_role_menu crm
      JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 5 AND r.groupe = false))
  ORDER BY (r.nom_role::text || ' '::text) || r.prenom_role::text, r.id_role;
  EXCEPTION WHEN undefined_table  THEN
        RAISE NOTICE 'Cet vue n''existe pas';
END
$$;

DO
$$
BEGIN
DROP VIEW contactfaune.v_nomade_observateurs_faune;
CREATE OR REPLACE VIEW contactfaune.v_nomade_observateurs_faune AS 
 SELECT DISTINCT r.id_role, r.nom_role, r.prenom_role
   FROM utilisateurs.t_roles r
  WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
           FROM utilisateurs.cor_roles cr
          WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
                   FROM utilisateurs.cor_role_menu crm
                  WHERE crm.id_menu = 11))
          ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
           FROM utilisateurs.cor_role_menu crm
      JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 11 AND r.groupe = false))
  ORDER BY r.nom_role, r.prenom_role, r.id_role;
EXCEPTION WHEN undefined_table  THEN
        RAISE NOTICE 'Cet vue n''existe pas';
END
$$;

DO
$$
BEGIN
DROP VIEW contactinv.v_nomade_observateurs_inv;
CREATE OR REPLACE VIEW contactinv.v_nomade_observateurs_inv AS 
 SELECT DISTINCT r.id_role, r.nom_role, r.prenom_role
   FROM utilisateurs.t_roles r
  WHERE (r.id_role IN ( SELECT DISTINCT cr.id_role_utilisateur
           FROM utilisateurs.cor_roles cr
          WHERE (cr.id_role_groupe IN ( SELECT crm.id_role
                   FROM utilisateurs.cor_role_menu crm
                  WHERE crm.id_menu = 11))
          ORDER BY cr.id_role_utilisateur)) OR (r.id_role IN ( SELECT crm.id_role
           FROM utilisateurs.cor_role_menu crm
      JOIN utilisateurs.t_roles r ON r.id_role = crm.id_role AND crm.id_menu = 11 AND r.groupe = false))
  ORDER BY r.nom_role, r.prenom_role, r.id_role;
  EXCEPTION WHEN undefined_table  THEN
        RAISE NOTICE 'Cet vue n''existe pas';
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

-- Supprimer la table bib_unités inutilisée
-- Supprimer la FK vers bib_unités dans t_roles
ALTER TABLE utilisateurs.t_roles DROP COLUMN id_unite RESTRICT;
-- Supprimer le champs organisme de t_roles (https://github.com/PnEcrins/UsersHub/issues/38)
ALTER TABLE utilisateurs.t_roles DROP COLUMN organisme RESTRICT;

ALTER TABLE utilisateurs.bib_unites SET SCHEMA save;


--------
--SAVE--
--------

--TODO AVANT  SUPPRESSION : 
--recréer les vues de GN1
--  contactfaune.v_nomade_observateurs_faune
--  contactflore.v_nomade_observateurs_flore
--  contactinv.v_nomade_observateurs_inv

--Rechercher les vues qui doivent être réécrites car pointant sur les tables déplacées dans le schéma save
SELECT dependent_ns.nspname as dependent_schema
, dependent_view.relname as dependent_view 
, source_ns.nspname as source_schema
, source_table.relname as source_table
, pg_attribute.attname as column_name
FROM pg_depend 
JOIN pg_rewrite ON pg_depend.objid = pg_rewrite.oid 
JOIN pg_class as dependent_view ON pg_rewrite.ev_class = dependent_view.oid 
JOIN pg_class as source_table ON pg_depend.refobjid = source_table.oid 
JOIN pg_attribute ON pg_depend.refobjid = pg_attribute.attrelid 
    AND pg_depend.refobjsubid = pg_attribute.attnum 
JOIN pg_namespace dependent_ns ON dependent_ns.oid = dependent_view.relnamespace
JOIN pg_namespace source_ns ON source_ns.oid = source_table.relnamespace
WHERE 
source_ns.nspname = 'save'
AND source_table.relname IN('cor_role_menu', 't_menus', 'bib_droits', 'cor_role_droit_application')
AND pg_attribute.attnum > 0 
--AND pg_attribute.attname = 'my_column'
ORDER BY 1,2;


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

