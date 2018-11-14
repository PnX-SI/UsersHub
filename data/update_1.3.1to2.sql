-- Ce script permet de recréer des tables qui simulent les tables de UsersHub V1 en se basant sur les tags
-- pour que les anciennes applications continuent à fonctionner

-- Associer les tags de type Liste à l'application GeoNature
-- INSERT INTO utilisateurs.cor_application_tag(id_application, id_tag) VALUES
-- (3,100)
-- ,(3,101)
-- ,(3,102)
-- ;
--> GIL : pas compris à quoi ça sert et je ne trouve nulle part de tags avec les id 100,101,102

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


------------
--TAGS GN2--
------------
--Insertion des tags V2 s'il n'existent pas déjà
DO
$$
BEGIN
INSERT INTO bib_tag_types (id_tag_type, tag_type_name, tag_type_desc) VALUES
(1, 'Object', 'Define a type object. Usually to define privileges on an object')
,(2, 'Action', 'Define a type action. Usually to define privileges for an action')
,(3, 'Privilege', 'Define a privilege level')
,(4, 'List', 'Define a type list to group anything')
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

-- nouveau type de tag "scope" fait séparément pour les bases comportant déjà les 4 premiers
DO
$$
BEGIN
INSERT INTO utilisateurs.bib_tag_types(id_tag_type, tag_type_name, tag_type_desc) VALUES
(5, 'Scope', 'Define a type Scope. Usually to define a scope for a action');
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

--mise à jour du id_tag_type qui était à 3 pour les tags de type scope
UPDATE utilisateurs.t_tags
SET id_tag_type = 5
WHERE tag_name IN('nothing','my data','my organism data','all data');

DO
$$
BEGIN
INSERT INTO utilisateurs.t_tags (id_tag, id_tag_type, tag_code, tag_name, tag_label, tag_desc) VALUES
(1, 3, '1', 'utilisateur', 'Utilisateur', 'Ne peut que consulter')
,(2, 3, '2', 'rédacteur', 'Rédacteur', 'Il possède des droit d''écriture pour créer des enregistrements')
,(3, 3, '3', 'référent', 'Référent', 'Utilisateur ayant des droits complémentaires au rédacteur (par exemple exporter des données ou autre)')
,(4, 3, '4', 'modérateur', 'Modérateur', 'Peu utilisé')
,(5, 3, '5', 'validateur', 'Validateur', 'Il valide bien sur')
,(6, 3, '6', 'administrateur', 'Administrateur', 'Il a tous les droits')
,(11, 2, 'C', 'create', 'Create', 'Can create/add new data')
,(12, 2, 'R', 'read', 'Read', 'Can read data')
,(13, 2, 'U', 'update', 'Update', 'Can update data')
,(14, 2, 'V', 'validate', 'Validate', 'Can validate data')
,(15, 2, 'E', 'export', 'Export', 'Can export data')
,(16, 2, 'D', 'delete', 'Delete', 'Can delete data')
,(20, 5, '0', 'nothing', 'Nothing', 'Cannot do anything')
,(21, 5, '1', 'my data', 'My data', 'Can do action only on my data')
,(22, 5, '2', 'my organism data', 'My organism data', 'Can do action only on my data and on my organism data')
,(23, 5, '3', 'all data', 'All data', 'Can do action on all data')
,(24, 4, NULL, 'observateurs occtax', 'Observateurs Occtax','Liste des observateurs dans le module Occtax')
;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;


---------
--MENUS--
---------
ALTER TABLE utilisateurs.cor_role_menu SET SCHEMA save;
ALTER TABLE utilisateurs.t_menus SET SCHEMA save;

--Récupérer les informations concernant les menus pour en faire des tags de type List
DO
$$
BEGIN
INSERT INTO utilisateurs.t_tags (id_tag, tag_code, id_tag_type, tag_name, tag_label, tag_desc)
SELECT max(t.id_tag)+m.id_menu, m.id_menu::character varying, 4, m.nom_menu, m.nom_menu, m.desc_menu
FROM utilisateurs.t_tags t, save.t_menus m
GROUP BY m.id_menu, m.nom_menu, m.nom_menu, m.desc_menu;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

DO
$$
BEGIN
INSERT INTO utilisateurs.cor_application_tag (id_tag, id_application)
SELECT t.id_tag, m.id_application 
FROM utilisateurs.t_tags t
JOIN save.t_menus  m ON m.nom_menu = t.tag_name
WHERE id_tag_type = 4;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

--cas particulier d'occtax qui n'a pas d'enregistrement dans t_menus de la v1
INSERT INTO utilisateurs.cor_application_tag (id_tag, id_application)
SELECT t.id_tag, (SELECT id_application FROM utilisateurs.t_applications WHERE nom_application IN('occtax')) 
FROM utilisateurs.t_tags t
JOIN save.t_menus  m ON m.nom_menu = t.tag_name
WHERE id_tag_type = 4
AND tag_name ILIKE 'observateurs occtax';
--TODO pour chaque module comme occtax. A creuser

DO
$$
BEGIN
INSERT INTO utilisateurs.cor_role_tag (id_role, id_tag)
SELECT  crm.id_role, t.id_tag 
FROM utilisateurs.t_tags t
JOIN save.cor_role_menu crm ON crm.id_menu = t.tag_code::integer
WHERE t.id_tag_type = 4;
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

-- Vue recréant l'equivalent de t_menus
CREATE OR REPLACE VIEW utilisateurs.t_menus AS 
SELECT 
 t.tag_code::integer AS id_menu,
 t.tag_name AS nom_menu,
 t.tag_desc AS desc_menu,
 c.id_application
FROM utilisateurs.bib_tag_types b
LEFT JOIN utilisateurs.t_tags t ON b.id_tag_type = t.id_tag_type
LEFT JOIN utilisateurs.cor_application_tag c ON c.id_tag = t.id_tag
WHERE b.id_tag_type = 4;

-- Vue recréant l'equivalent de cor_role_menu
--TODO : id_tag et id_menu ne sont pas correspondant updater les id_menu de cor_role_menu
CREATE OR REPLACE VIEW utilisateurs.cor_role_menu AS 
SELECT 
 DISTINCT
 c.id_role,
 t.tag_code::integer AS id_menu
FROM utilisateurs.cor_role_tag c
JOIN utilisateurs.t_tags t ON t.id_tag = c.id_tag
WHERE t.id_tag_type = 4;


----------
--DROITS--
----------
ALTER TABLE utilisateurs.bib_droits SET SCHEMA save;
ALTER TABLE utilisateurs.cor_role_droit_application SET SCHEMA save;
-- Associer des roles aux tags de type Droits V1
-- INSERT INTO utilisateurs.cor_role_tag(id_role, id_tag) VALUES
-- (20002,2)
-- ;

-- Associer les tags de type Droits V1 à l'application GeoNature
-- Si il n'y a pas d'application définie, alors le tag devrait s'appliquer à toutes les applications
-- INSERT INTO utilisateurs.cor_application_tag(id_application, id_tag) VALUES
-- (3,2)
-- ;
--> GIL pas trop compris à quoi servent ces 2 insert

-- Vue recréant l'equivalent de bib_droits à partir des tags existants
CREATE OR REPLACE VIEW utilisateurs.bib_droits AS 
SELECT 
 t.id_tag AS id_droit,
 t.tag_name AS nom_droit,
 t.tag_desc AS desc_droit
FROM utilisateurs.bib_tag_types b
JOIN utilisateurs.t_tags t ON b.id_tag_type = t.id_tag_type
WHERE b.id_tag_type = 3;

--création d'un droit zéro existant en v1
DO
$$
BEGIN
INSERT INTO utilisateurs.t_tags (id_tag, id_tag_type, tag_code, tag_name, tag_label, tag_desc) VALUES
(0, 3, '0', 'aucun', 'aucun', 'aucun droit');
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;

--Table qui remplace la table cor_role_droit_application de la V1
-- CREATE TABLE IF NOT EXISTS utilisateurs.cor_role_tag_application (
--     id_role integer NOT NULL,
--     id_tag integer NOT NULL,
--     id_application integer NOT NULL
-- );
-- COMMENT ON TABLE cor_role_tag_application IS 'Equivalent de l''ancienne cor_role_droit_application. Permet de stocker les droits par rôle et applications pour rester compatible avec UHV1';

-- ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_pkey PRIMARY KEY (id_role, id_tag, id_application);
-- ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_application_fkey FOREIGN KEY (id_application) REFERENCES utilisateurs.t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;
-- ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_tag_fkey FOREIGN KEY (id_tag) REFERENCES utilisateurs.t_tags(id_tag) ON UPDATE CASCADE ON DELETE CASCADE;
-- ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_role_fkey FOREIGN KEY (id_role) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;

--> GIL : je préfère un mécanisme utilisant les tables existantes. La table cor_app_privileges permet de stocker ces infos
--> A VOIR si interférences avec le cruved et si modif à faire pour dans GN2 et UHV2

--on insert les informations de l'ancienne cor_role_droit_application dans cor_app_privileges
--on postule que les id_tag de 0 à 6 et les id_droits sont correspondants
--La numérotation des tags lors de leur création initiale avait intégré cette question de la migration UH1 to UH2
INSERT INTO cor_app_privileges (id_tag_action, id_tag_object, id_application, id_role)
SELECT id_droit as id_tag_action, 3 as id_tag_object, id_application, id_role
FROM save.cor_role_droit_application;

-- Vue recréant l'équivalent de cor_role_droit_application
CREATE OR REPLACE VIEW utilisateurs.cor_role_droit_application AS 
SELECT 
 cap.id_role,
 cap.id_tag_action as id_droit, 
 cap.id_application
FROM utilisateurs.cor_app_privileges cap
WHERE id_tag_action <=6;


----------
--AUTRES--
----------
--Correction de la Vue v_usersaction_forall_gn_modules afin d'obtenir le cruved de groupe
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
             JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role OR g.id_role_groupe=u.id_role --seul point modifié, à vérifier
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

DROP VIEW v_userslist_forall_menu;
CREATE OR REPLACE VIEW v_userslist_forall_menu AS 
SELECT a.groupe, a.id_role, a.identifiant, a.nom_role, a.prenom_role, (upper(a.nom_role::text) || ' '::text) || a.prenom_role::text AS nom_complet, a.desc_role, a.pass, a.pass_plus, a.email, a.id_organisme, a.organisme, a.id_unite, a.remarques, a.pn, a.session_appli, a.date_insert, a.date_update, a.id_menu
FROM (  SELECT u.groupe, u.id_role, u.identifiant, u.nom_role, u.prenom_role, u.desc_role, u.pass, u.pass_plus, u.email, u.id_organisme, o.nom_organisme AS organisme, u.id_unite, u.remarques, u.pn, u.session_appli, u.date_insert, u.date_update, c.id_menu
        FROM utilisateurs.t_roles u
        JOIN utilisateurs.cor_role_menu c ON c.id_role = u.id_role
        LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
        WHERE u.groupe = false
UNION 
        SELECT u.groupe, u.id_role, u.identifiant, u.nom_role, u.prenom_role, u.desc_role, u.pass, u.pass_plus, u.email, u.id_organisme, o.nom_organisme AS organisme, u.id_unite, u.remarques, u.pn, u.session_appli, u.date_insert, u.date_update, c.id_menu
        FROM utilisateurs.t_roles u
        JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role
        JOIN utilisateurs.cor_role_menu c ON c.id_role = g.id_role_groupe
        LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
        WHERE u.groupe = false
) a;

DROP VIEW v_userslist_forall_applications;
CREATE OR REPLACE VIEW v_userslist_forall_applications AS 
SELECT a.groupe, a.id_role, a.identifiant, a.nom_role, a.prenom_role, a.desc_role, a.pass, a.pass_plus, a.email, a.id_organisme, a.organisme, a.id_unite, a.remarques, a.pn, a.session_appli, a.date_insert, a.date_update, max(a.id_droit) AS id_droit_max, a.id_application
FROM    (       SELECT u.groupe, u.id_role, u.identifiant, u.nom_role, u.prenom_role, u.desc_role, u.pass, u.pass_plus, u.email, u.id_organisme, o.nom_organisme AS organisme, u.id_unite, u.remarques, u.pn, u.session_appli, u.date_insert, u.date_update, c.id_droit, c.id_application
                FROM utilisateurs.t_roles u
                JOIN utilisateurs.cor_role_droit_application c ON c.id_role = u.id_role
                LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
                WHERE u.groupe = false
        UNION 
                SELECT u.groupe, u.id_role, u.identifiant, u.nom_role, u.prenom_role, u.desc_role, u.pass, u.pass_plus, u.email, u.id_organisme, o.nom_organisme AS organisme, u.id_unite, u.remarques, u.pn, u.session_appli, u.date_insert, u.date_update, c.id_droit, c.id_application
                FROM utilisateurs.t_roles u
                JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role
                JOIN utilisateurs.cor_role_droit_application c ON c.id_role = g.id_role_groupe
                LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
                WHERE u.groupe = false
        ) a
GROUP BY a.groupe, a.id_role, a.identifiant, a.nom_role, a.prenom_role, a.desc_role, a.pass, a.pass_plus, a.email, a.id_organisme, a.organisme, a.id_unite, a.remarques, a.pn, a.session_appli, a.date_insert, a.date_update, a.id_application;

--On essaie de recréer une vue qui n'existe pas dans toutes les bases
--Si elle n'existe pas une erreur est levée est la création ne se fait pas.
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

-- Supprimer le champs organisme de t_roles (https://github.com/PnEcrins/UsersHub/issues/38)
ALTER TABLE utilisateurs.t_roles DROP COLUMN organisme RESTRICT;

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
-- Supprimer la table cor_role_menu
--DROP TABLE save.cor_role_menu;
-- Supprimer la table t_menus
--DROP TABLE save.t_menus;
-- Supprime la table cor_role_droit_application
--DROP TABLE save.cor_role_droit_application;
-- Supprime la table bib_droits
--DROP TABLE save.bib_droits;

