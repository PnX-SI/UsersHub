----------------
--MINIMAL DATA--
----------------

SET search_path = utilisateurs, pg_catalog;

-- Insérer les applications de base liées à GeoNature
INSERT INTO t_applications (id_application, code_application, nom_application, desc_application, id_parent) VALUES 
(1, 'UH', 'UsersHub', 'Application permettant d''administrer la présente base de données.', NULL)
;
SELECT pg_catalog.setval('t_applications_id_application_seq', (SELECT max(id_application)+1 FROM utilisateurs.t_applications), false);	

INSERT INTO t_profils (id_profil, code_profil, nom_profil, desc_profil) VALUES
(0, '0', 'Aucun', 'Aucun droit')
,(1, '1', 'Lecteur', 'Ne peut que consulter/ou acceder')
,(2, '2', 'Rédacteur', 'Il possède des droit d''écriture pour créer des enregistrements')
,(3, '3', 'Référent', 'Utilisateur ayant des droits complémentaires au rédacteur (par exemple exporter des données ou autre)')
,(4, '4', 'Modérateur', 'Peu utilisé')
,(5, '5', 'Validateur', 'Il valide bien sur')
,(6, '6', 'Administrateur', 'Il a tous les droits');
SELECT pg_catalog.setval('t_profils_id_profil_seq', (SELECT max(id_profil)+1 FROM utilisateurs.t_profils), false);

INSERT INTO utilisateurs.cor_profil_for_app (id_profil, id_application) VALUES
(6, 1)
,(3, 1)
;
