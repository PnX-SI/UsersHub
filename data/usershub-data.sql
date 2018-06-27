--------
--DATA--
--------

INSERT INTO bib_organismes (nom_organisme, adresse_organisme, cp_organisme, ville_organisme, tel_organisme, fax_organisme, email_organisme, id_organisme) VALUES 
('Parc National des Ecrins', 'Domaine de Charance', '05000', 'GAP', '04 92 40 20 10', '', '', 1)
,('Autre', '', '', '', '', '', '', -1)
;

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

INSERT INTO t_applications (id_application, nom_application, desc_application, id_parent) VALUES 
(1, 'UsersHub', 'Application permettant d''administrer la présente base de données.',NULL)
,(2, 'TaxHub', 'Application permettant d''administrer la liste des taxons.',NULL)
,(14, 'GeoNature', 'Application permettant la consultation et la gestion des relevés faune et flore.',NULL)
,(15, 'OccTax (GeoNature2)', 'Module OccTax (contact faune-flore-fonge) de GeoNature', 14)
;
PERFORM pg_catalog.setval('t_applications_id_application_seq', 15, true);

INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, id_unite, pn, session_appli, date_insert, date_update, id_organisme, remarques) VALUES 
(true, 20001, NULL, 'Grp_socle 2', NULL, 'Bureau d''étude socle 2', NULL, NULL, -1, true, NULL, NULL, NULL, NULL, 'Groupe à droit étendu')
,(true, 20002, NULL, 'Grp_en_poste', NULL, 'Tous les agents en poste au PN', NULL, NULL, -1, true, NULL, NULL, NULL, NULL,'groupe test')
,(true, 20003, NULL, 'Grp_socle 1', NULL, 'Bureau d''étude socle 1', NULL, NULL, -1, true, NULL, NULL, NULL, NULL,'Groupe à droit limité')
;
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, organisme, id_unite, pn, session_appli, date_insert, date_update, id_organisme, remarques, pass_plus) VALUES 
(false, 1, 'admin', 'Administrateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, 'Autre', -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier', '$2y$13$TMuRXgvIg6/aAez0lXLLFu0lyPk4m8N55NDhvLoUHh/Ar3rFzjFT.')
,(false, 2, 'agent', 'Agent', 'test', NULL, 'b33aed8f3134996703dc39f9a7c95783', NULL, 'Autre', -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false, 3, 'partenaire', 'Partenaire', 'test', NULL, '5bd40a8524882d75f3083903f2c912fc', NULL, 'Autre', -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false,4, 'pierre.paul', 'Paul', 'Pierre', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, 'Autre', -1, false, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false,5, 'validateur', 'validateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, 'Autre', -1, false, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
;

INSERT INTO cor_roles (id_role_groupe, id_role_utilisateur) 
VALUES (20002, 1)
,(20002, 2)
,(20002, 4)
,(20002, 5)
;

INSERT INTO bib_tag_types (id_tag_type, tag_type_name, tag_type_desc) VALUES
(1, 'Object', 'Define a type object. Usually to define privileges on an object')
,(2, 'Action', 'Define a type action. Usually to define privileges for an action')
,(3, 'Privilege', 'Define a privilege level')
,(4, 'Liste', 'Define a type liste for grouping anything')
,(5, 'Scope','Define a type scope for CRUVED data')
;

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
,(21, 5, '1', 'my data', 'My data', 'Can do action only on my data')
,(22, 5, '2', 'my organism data', 'My organism data', 'Can do action only on my data and on my organism data')
,(23, 5, '3', 'all data', 'All data', 'Can do action on all data')
,(100, 4, NULL, 'observateurs flore', 'Observateurs flore','Liste des observateurs pour les protocoles flore')
,(101, 4, NULL, 'observateurs faune', 'Observateurs faune','Liste des observateurs pour les protocoles faune')
,(102, 4, NULL, 'observateurs aigle', 'Observateurs aigle','Liste des observateurs pour le protocole suivi de la reproduction de l''aigle royal')
;
PERFORM pg_catalog.setval('t_tags_id_tag_seq', 103, true);

INSERT INTO cor_role_tag (id_role, id_tag) VALUES
--Liste des observateurs faune
(1,101)
,(20002,101)
,(5,101)
-- --Liste des observateurs flore
,(2,100)
,(5,100)
;

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
