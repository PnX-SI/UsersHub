----------------
--MINIMAL DATA--
----------------

SET search_path = utilisateurs, pg_catalog;

-- Insérer les applications de base liées à GeoNature
INSERT INTO t_applications (id_application, nom_application, desc_application, id_parent) VALUES 
(1, 'UsersHub', 'Application permettant d''administrer la présente base de données.',NULL)
,(2, 'TaxHub', 'Application permettant d''administrer la liste des taxons.',NULL)
,(3, 'GeoNature', 'Application permettant la consultation et la gestion des relevés faune et flore.',NULL)
,(4, 'OccTax (GeoNature2)', 'Module OccTax (contact faune-flore-fonge) de GeoNature', 3)
;
SELECT pg_catalog.setval('t_applications_id_application_seq', (SELECT max(id_application)+1 FROM utilisateurs.t_applications), false);	

-- Insérer les types de tag utilisés par GeoNature
INSERT INTO bib_tag_types (id_tag_type, tag_type_name, tag_type_desc) VALUES
(1, 'Object', 'Define a type object. Usually to define privileges on an object')
,(2, 'Action', 'Define a type action. Usually to define privileges for an action')
,(3, 'Privilege', 'Define a privilege level')
,(4, 'List', 'Define a type list to group anything')
,(5, 'Scope', 'Define a type scope for CRUVED data')
;

-- 
INSERT INTO t_tags (id_tag, id_tag_type, tag_code, tag_name, tag_label, tag_desc) VALUES
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
,(4, 2, 'E', 'export', 'Export', 'Can export data')
,(16, 2, 'D', 'delete', 'Delete', 'Can delete data')
,(20, 3, '0', 'nothing', 'Nothing', 'Cannot do anything')
,(21, 5, '1', 'my data', 'My data', 'Can do action only on my data')
,(22, 5, '2', 'my organism data', 'My organism data', 'Can do action only on my data and on my organism data')
,(23, 5, '3', 'all data', 'All data', 'Can do action on all data')
,(24, 4, NULL, 'observateurs flore', 'Observateurs flore','Liste des observateurs pour les protocoles flore')
,(25, 4, NULL, 'observateurs faune', 'Observateurs faune','Liste des observateurs pour les protocoles faune')
,(26, 4, NULL, 'observateurs aigle', 'Observateurs aigle','Liste des observateurs pour le protocole suivi de la reproduction de l''aigle royal')
;
SELECT pg_catalog.setval('t_tags_id_tag_seq', (SELECT max(id_tag)+1 FROM utilisateurs.t_tags), false);	
