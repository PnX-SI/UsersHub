-- Ce script permet de recréer des tables qui simulent les tables de UsersHub V1 en se basant sur les tags
-- pour que les anciennes applications continuent à fonctionner
-- @TODO : ATTENTION, il manque les récupération des données avant de supprimer les anciennes tables

-- Supprimer le champs organisme de t_roles (https://github.com/PnEcrins/UsersHub/issues/38)
ALTER TABLE utilisateurs.t_roles DROP COLUMN organisme RESTRICT;

-- Associer les tags de type Liste à l'application GeoNature
INSERT INTO utilisateurs.cor_application_tag(id_application, id_tag) VALUES
(14,100)
,(14,101)
,(14,102)
;

-- Supprimer la table t_menus
DROP TABLE utilisateurs.t_menus CASCADE;

-- Vue recréant l'equivalent de t_menus
CREATE OR REPLACE VIEW utilisateurs.t_menus AS 
SELECT 
 t.id_tag AS id_menu,
 t.tag_name AS nom_menu,
 t.tag_desc AS desc_menu,
 c.id_application
FROM utilisateurs.bib_tag_types b
LEFT JOIN utilisateurs.t_tags t ON b.id_tag_type = t.id_tag_type
LEFT JOIN utilisateurs.cor_application_tag c ON c.id_tag = t.id_tag
WHERE b.id_tag_type = 4

-- Supprimer la table cor_role_menu
DROP TABLE utilisateurs.cor_role_menu CASCADE;

-- Vue recréant l'equivalent de cor_role_menu
CREATE OR REPLACE VIEW utilisateurs.cor_role_menu AS 
SELECT 
 DISTINCT
 c.id_role,
 c.id_tag AS id_menu
FROM utilisateurs.cor_role_tag c
JOIN utilisateurs.t_menus v ON v.id_menu = c.id_tag

-- Associer des roles aux tags de type Droits V1
INSERT INTO utilisateurs.cor_role_tag(id_role, id_tag) VALUES
(20002,2)
;

-- Associer les tags de type Droits V1 à l'application GeoNature
-- Si il n'y a pas d'application définie, alors le tag devrait s'appliquer à toutes les applications
INSERT INTO utilisateurs.cor_application_tag(id_application, id_tag) VALUES
(14,2)
;

-- Supprimer la table bib_droits
DROP TABLE utilisateurs.bib_droits CASCADE;

-- Vue recréant l'equivalent de bib_droits
CREATE OR REPLACE VIEW utilisateurs.bib_droits AS 
SELECT 
 t.id_tag AS id_droit,
 t.tag_name AS nom_droit,
 t.tag_desc AS desc_droit
FROM utilisateurs.bib_tag_types b
JOIN utilisateurs.t_tags t ON b.id_tag_type = t.id_tag_type
WHERE b.id_tag_type = 3

--Table qui compense la table cor_role_droit_application de la V1
CREATE TABLE IF NOT EXISTS utilisateurs.cor_role_tag_application (
    id_role integer NOT NULL,
    id_tag integer NOT NULL,
    id_application integer NOT NULL
);
COMMENT ON TABLE cor_role_tag_application IS 'Equivalent de l''ancienne cor_role_droit_application. Permet de stocker les droits par rôle et applications pour rester compatible avec UHV1';

ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_pkey PRIMARY KEY (id_role, id_tag, id_application);
ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_application_fkey FOREIGN KEY (id_application) REFERENCES utilisateurs.t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_tag_fkey FOREIGN KEY (id_tag) REFERENCES utilisateurs.t_tags(id_tag) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_role_fkey FOREIGN KEY (id_role) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;

-- Vue recréant l'equivalent de cor_role_droit_application
CREATE OR REPLACE VIEW utilisateurs.cor_role_droit_application AS 
SELECT 
 c.id_role,
 c.id_tag as id_droit, 
 c.id_application
FROM utilisateurs.cor_role_tag_application c

-- Associe les portées des données à un type de tag "scope"
INSERT INTO utilisateurs.bib_tag_types(id_tag_type,tag_type_name,tag_type_desc) VALUES
(5,'scope','Define a type scope for CRUVED data')

UPDATE utilisateurs.t_tags
set 
id_tag = 22,
id_tag_type = 5,
tag_code = '2',
tag_name = 'my organism data',
tag_label = 'My organism data',
tag_desc = 'Can do action only on my data and on my organism data'
where 
id_tag = 22;

UPDATE utilisateurs.t_tags
set 
id_tag = 21,
id_tag_type = 5,
tag_code = '1',
tag_name = 'my data',
tag_label = 'My data',
tag_desc = 'Can do action only on my data'
where 
id_tag = 21;

UPDATE utilisateurs.t_tags
set 
id_tag = 23,
id_tag_type = 5,
tag_code = '3',
tag_name = 'all data',
tag_label = 'All data',
tag_desc = 'Can do action on all data'
where 
id_tag = 23;

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
