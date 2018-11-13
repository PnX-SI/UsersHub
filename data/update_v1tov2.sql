--Ebauche migration V1 to V2
DO
$$
BEGIN
INSERT INTO utilisateurs.bib_tag_types(id_tag_type, tag_type_name, tag_type_desc) VALUES
(5, 'Scope', 'Define a type Scope. Usually to define a scope for a action');
EXCEPTION WHEN unique_violation  THEN
        RAISE NOTICE 'Tentative d''insertion de valeur existante';
END
$$;
UPDATE utilisateurs.t_tags
SET id_tag_type = 5
WHERE tag_name IN('nothing','my data','my organism data','all data');