-- Ce script permet de mettre à jour la structure et le contenu du schéma "utilisateurs" de UsersHub
-- de la version 2.0.3 à la version 2.0.4

-- Suppression de la génération automatique et l'obligation d'un uuid pour les organismes (bib_organismes)
ALTER TABLE utilisateurs.bib_organismes ALTER COLUMN uuid_organisme DROP NOT NULL;
ALTER TABLE utilisateurs.bib_organismes ALTER COLUMN uuid_organisme DROP DEFAULT;
