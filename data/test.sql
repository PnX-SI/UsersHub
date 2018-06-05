-- test v1 à v2

DROP TABLE utilisateurs.t_menus CASCADE;

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

select * from utilisateurs.t_menus

DROP TABLE utilisateurs.cor_role_menu CASCADE;

CREATE OR REPLACE VIEW utilisateurs.cor_role_menu AS 
SELECT 
 DISTINCT
 c.id_role,
 c.id_tag AS id_menu
FROM utilisateurs.cor_role_tag c
JOIN utilisateurs.t_menus v ON v.id_menu = c.id_tag

select * from utilisateurs.cor_role_menu

DROP TABLE utilisateurs.bib_droits CASCADE;

CREATE OR REPLACE VIEW utilisateurs.bib_droits AS 
SELECT 
 t.id_tag AS id_droit,
 t.tag_name AS nom_droit,
 t.tag_desc AS desc_droit
FROM utilisateurs.bib_tag_types b
JOIN utilisateurs.t_tags t ON b.id_tag_type = t.id_tag_type
WHERE b.id_tag_type = 3

Select * from utilisateurs.bib_droits

CREATE TABLE IF NOT EXISTS utilisateurs.cor_role_tag_application (
    id_role integer NOT NULL,
    id_tag integer NOT NULL,
    id_application integer NOT NULL
);

ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_pkey PRIMARY KEY (id_role, id_tag, id_application);
ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_application_fkey FOREIGN KEY (id_application) REFERENCES utilisateurs.t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_tag_fkey FOREIGN KEY (id_tag) REFERENCES utilisateurs.t_tags(id_tag) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY utilisateurs.cor_role_tag_application ADD CONSTRAINT cor_role_tag_application_id_role_fkey FOREIGN KEY (id_role) REFERENCES utilisateurs.t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;

select * from utilisateurs.cor_role_tag_application

CREATE OR REPLACE VIEW utilisateurs.cor_role_droit_application AS 
SELECT 
 c.id_role,
 c.id_tag as id_droit, 
 c.id_application
FROM utilisateurs.cor_role_tag_application c
 

select * from utilisateurs.cor_role_droit_application
