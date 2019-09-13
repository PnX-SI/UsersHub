---------------
--SAMPLE DATA--
---------------

SET search_path = utilisateurs, pg_catalog;

-- Insertion de 2 organismes 
INSERT INTO bib_organismes (nom_organisme, adresse_organisme, cp_organisme, ville_organisme, tel_organisme, fax_organisme, email_organisme, id_organisme) VALUES 
('Autre', '', '', '', '', '', '', -1)
;
INSERT INTO bib_organismes (nom_organisme, adresse_organisme, cp_organisme, ville_organisme, tel_organisme) VALUES 
('ma structure test', 'Rue des bois', '00000', 'VILLE', '00-00-99-00-99');

-- Insertion de roles de type GROUPE de base pour GeoNature
--TODO revoir l'insertion des organisme et des identifiants
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, date_insert, date_update, id_organisme, remarques) VALUES 
(true, 7, NULL, 'Grp_en_poste', NULL, 'Tous les agents en poste dans la structure', NULL, NULL, NULL, NULL, NULL, 'Groupe des agents de la structure avec droits d''écriture limité')
,(true, 9, NULL, 'Grp_admin', NULL, 'Tous les administrateurs', NULL, NULL, NULL, NULL, NULL, 'Groupe à droit total')
;
-- Insertion de roles de type UTILISATEUR pour GeoNature
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, date_insert, date_update, id_organisme, remarques, pass_plus) VALUES 
(false, 1, 'admin', 'Administrateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, NULL, NULL, -1, 'utilisateur test à modifier', '$2y$13$TMuRXgvIg6/aAez0lXLLFu0lyPk4m8N55NDhvLoUHh/Ar3rFzjFT.')
,(false, 2, 'agent', 'Agent', 'test', NULL, 'b33aed8f3134996703dc39f9a7c95783', NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false, 3, 'partenaire', 'Partenaire', 'test', NULL, '5bd40a8524882d75f3083903f2c912fc', NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false, 4, 'pierre.paul', 'Paul', 'Pierre', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
,(false, 5, 'validateur', 'Validateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', NULL, NULL, NULL, -1, 'utilisateur test à modifier ou supprimer', NULL)
;
-- Ajuster la séquence de t_roles après insertion des données
SELECT pg_catalog.setval('t_roles_id_role_seq', (SELECT max(id_role)+1 FROM utilisateurs.t_roles), false);

-- Affectation des utilisateurs exemple dans des groupes
INSERT INTO cor_roles (id_role_groupe, id_role_utilisateur) VALUES 
(7, 1)
,(9, 1)
,(7, 2)
,(7, 4)
,(7, 5)
;

INSERT INTO cor_role_app_profil (id_role, id_application, id_profil) VALUES
(9, 1, 6) --admin UsersHub
;
