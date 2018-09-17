---------------
--SAMPLE DATA--
---------------

SET search_path = utilisateurs, pg_catalog;

-- Insertion de 2 organismes 
INSERT INTO bib_organismes (nom_organisme, adresse_organisme, cp_organisme, ville_organisme, tel_organisme, fax_organisme, email_organisme, id_organisme) VALUES 
('Parc National des Ecrins', 'Domaine de Charance', '05000', 'GAP', '04-92-40-20-10', '', '', 1)
,('Autre', '', '', '', '', '', '', -1)
;
-- Ajuster la séquence de bib_organismes après insertion des 2 lignes
SELECT pg_catalog.setval('bib_organismes_id_seq', (SELECT max(id_organisme)+1 FROM utilisateurs.bib_organismes), false);

-- Insertion d'une liste d'unités - Non utilisé
--INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES 
--('Virtuel', NULL, NULL, NULL, NULL, NULL, NULL, 1)
--,('Personnels partis', NULL, NULL, NULL, NULL, NULL, NULL, 2)
--,('Stagiaires', NULL, NULL, '', '', NULL, NULL, 3)
--,('Secretariat général', '', '', '', '', NULL, NULL, 4)
--,('Service scientifique', '', '', '', '', NULL, NULL, 5)
--,('Service SI', '', '', '', '', NULL, NULL, 6)
--,('Service Communication', '', '', '', '', NULL, NULL, 7)
--,('Conseil scientifique', '', '', '', NULL, NULL, NULL, 8)
--,('Conseil d''administration', '', '', '', NULL, NULL, NULL, 9)
--,('Partenaire fournisseur', NULL, NULL, NULL, NULL, NULL, NULL, 10)
--,('Autres', NULL, NULL, NULL, NULL, NULL, NULL, -1)
--;

-- Insertion de roles de type GROUPE de base pour GeoNature
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, id_unite, pn, session_appli, date_insert, date_update, id_organisme, remarques) VALUES 
(true, 6, NULL, 'Grp_socle 2', NULL, 'Bureau d''étude socle 2', NULL, NULL, -1, true, NULL, NULL, NULL, NULL, 'Groupe à droit étendu sur les données de son organisme')
,(true, 7, NULL, 'Grp_en_poste', NULL, 'Tous les agents en poste dans la structure', NULL, NULL, -1, true, NULL, NULL, NULL, NULL, 'Groupe des agents de la structure avec droits d''écriture limité')
,(true, 8, NULL, 'Grp_socle 1', NULL, 'Bureau d''étude socle 1', NULL, NULL, -1, true, NULL, NULL, NULL, NULL, 'Groupe à droit limité sur ses données')
,(true, 9, NULL, 'Grp_admin', NULL, 'Tous les administrateurs', NULL, NULL, -1, true, NULL, NULL, NULL, NULL, 'Groupe à droit total')
;
-- Insertion de roles de type UTILISATEUR pour GeoNature
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, id_unite, pn, session_appli, date_insert, date_update, id_organisme, remarques, pass_plus) VALUES 
(false, 1, 'admin', 'Administrateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL,  -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier', '$2y$13$TMuRXgvIg6/aAez0lXLLFu0lyPk4m8N55NDhvLoUHh/Ar3rFzjFT.')
,(false, 2, 'agent', 'Agent', 'test', NULL, 'b33aed8f3134996703dc39f9a7c95783', NULL,  -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false, 3, 'partenaire', 'Partenaire', 'test', NULL, '5bd40a8524882d75f3083903f2c912fc', NULL,  -1, true, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false, 4, 'pierre.paul', 'Paul', 'Pierre', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL,  -1, false, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false, 5, 'validateur', 'Validateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL,  -1, false, NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
;
-- Ajuster la séquence de t_roles après insertion des données
SELECT pg_catalog.setval('t_roles_id_role_seq', (SELECT max(id_role)+1 FROM utilisateurs.t_roles), false);

-- Affectation des utilisateurs exemple dans des groupes
INSERT INTO cor_roles (id_role_groupe, id_role_utilisateur) 
VALUES 
(7, 1)
,(9, 1)
,(7, 2)
,(7, 4)
,(7, 5)
;

INSERT INTO cor_role_tag (id_role, id_tag) VALUES
-- Liste des observateurs Occtax
(1,24)
,(7,24)
,(2,24)
,(5,24)
;

INSERT INTO cor_role_tag_application (id_role, id_tag, id_application) VALUES
--- Groupe administrateur sur UsersHub et TaxHub
(9,6,1)
,(9,6,2)
;

-- Exemples de CRUVED pour GeoNature
INSERT INTO cor_app_privileges (id_tag_action, id_tag_object, id_application, id_role) VALUES
--Administrateur sur GeoNature
(11, 23, 3, 9)
,(12, 23, 3, 9)
,(13, 23, 3, 9)
,(14, 23, 3, 9)
,(15, 23, 3, 9)
,(16, 23, 3, 9)
--Validateur général sur tout GeoNature
,(14, 23, 3, 5)
--Validateur pour son organisme sur Occtax
--,(14, 22, 15, 4) --Droit supprimé car appli Occtax créé par l'installation du module
--CRUVED du groupe en poste sur tout GeoNature
,(11, 23, 3, 7)
,(12, 22, 3, 7)
,(13, 21, 3, 7)
,(15, 22, 3, 7)
,(16, 21, 3, 7)
--Groupe bureau d''étude socle 2 sur tout GeoNature
,(11, 23, 3, 6)
,(12, 22, 3, 6)
,(13, 21, 3, 6)
,(15, 22, 3, 6)
,(16, 21, 3, 6)
--Groupe bureau d''étude socle 1 sur tout GeoNature
,(11, 23, 3, 8)
,(12, 21, 3, 8)
,(13, 21, 3, 8)
,(15, 21, 3, 8)
,(16, 21, 3, 8)
;
