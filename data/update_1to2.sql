-- Ce script permet de recréer des tables qui simulent les tables de UsersHub V1 en se basant sur les tags
-- pour que les anciennes applications continuent à fonctionner
-- @TODO : ATTENTION, il manque les récupération des données avant de supprimer les anciennes tables

-- Associer les tags de type Liste à l'application GeoNature
INSERT INTO utilisateurs.cor_application_tag(id_application, id_tag) VALUES
(14,100)
,(14,101)
,(14,102)
;

-- Supprimer la table t_menus
DROP TABLE utilisateurs.t_menus;

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
DROP TABLE utilisateurs.cor_role_menu;

-- Vue recréant l'equivalent de cor_role_menu
CREATE OR REPLACE VIEW utilisateurs.cor_role_menu AS 
SELECT 
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
DROP TABLE utilisateurs.bib_droits;

-- Vue recréant l'equivalent de bib_droits
CREATE OR REPLACE VIEW utilisateurs.bib_droits AS 
SELECT 
 t.id_tag AS id_droit,
 t.tag_name AS nom_droit,
 t.tag_desc AS desc_desc_droit
FROM utilisateurs.bib_tag_types b
JOIN utilisateurs.t_tags t ON b.id_tag_type = t.id_tag_type
WHERE b.id_tag_type = 3

-- Vue recréant l'equivalent de cor_role_droit_application
CREATE OR REPLACE VIEW utilisateurs.cor_role_droit_application AS 
SELECT 
 c.id_role,
 b.id_droit, 
 ct.id_application
FROM utilisateurs.cor_role_tag c
JOIN utilisateurs.bib_droits b ON b.id_droit = c.id_tag
JOIN utilisateurs.cor_application_tag ct ON ct.id_tag = c.id_tag

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


