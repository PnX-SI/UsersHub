
ALTER TABLE utilisateurs.cor_role_app_profil ADD is_default_group_for_app boolean NOT NULL DEFAULT (FALSE);

CREATE OR REPLACE FUNCTION utilisateurs.check_is_default_group_for_app_is_grp_and_unique(id_app integer, id_grp integer, is_default boolean)
RETURNS boolean AS
$BODY$
BEGIN
    IF is_default IS TRUE THEN
        IF (
            SELECT DISTINCT TRUE
            FROM utilisateurs.cor_role_app_profil
            WHERE id_application = id_app AND is_default_group_for_app IS TRUE
        ) IS TRUE THEN
            RETURN FALSE;
        ELSIF (SELECT TRUE FROM utilisateurs.t_roles WHERE id_role = id_grp AND groupe IS TRUE) IS NULL THEN
            RETURN FALSE;
        ELSE
          RETURN TRUE;
        END IF;
    END IF;
    RETURN TRUE;
  END
$BODY$
  LANGUAGE plpgsql IMMUTABLE
  COST 100;


ALTER TABLE utilisateurs.cor_role_app_profil ADD CONSTRAINT check_is_default_group_for_app_is_grp_and_unique
    CHECK (utilisateurs.check_is_default_group_for_app_is_grp_and_unique(id_application, id_role, is_default_group_for_app));
