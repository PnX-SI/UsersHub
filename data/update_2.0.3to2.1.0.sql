CREATE INDEX i_utilisateurs_groupe
  ON utilisateurs.t_roles
  USING btree
  (groupe);

CREATE INDEX i_utilisateurs_nom_prenom
  ON utilisateurs.t_roles
  USING btree
  (nom_role, prenom_role);

CREATE INDEX i_utilisateurs_active
  ON utilisateurs.t_roles
  USING btree
  (active);



DROP TRIGGER IF EXISTS tri_modify_date_insert_temp_roles ON utilisateurs.temp_users;

CREATE TRIGGER tri_modify_date_insert_temp_roles
    BEFORE INSERT
    ON utilisateurs.temp_users
    FOR EACH ROW
    EXECUTE PROCEDURE utilisateurs.modify_date_insert();


ALTER TABLE utilisateurs.cor_role_app_profil ADD COLUMN is_default_group_for_app boolean NOT NULL DEFAULT (FALSE);


DROP TABLE IF EXISTS utilisateurs.temp_users;

CREATE TABLE IF NOT EXISTS utilisateurs.temp_users
(

    id_temp_user SERIAL NOT NULL,

    groupe boolean NOT NULL DEFAULT false,
    token_role text,
    identifiant character varying(100),
    nom_role character varying(50),
    prenom_role character varying(50),
    desc_role text,
    password text,
    pass_md5 text,
    email character varying(250),
    organisme character(32),
    id_organisme integer,
    id_application integer,
    remarques text,
    champs_addi jsonb,
    session_appli character varying(50),
    date_insert timestamp without time zone,
    date_update timestamp without time zone,

    CONSTRAINT pk_temp_users     PRIMARY KEY (id_temp_user),

    CONSTRAINT temp_user_id_organisme_fkey FOREIGN KEY (id_application)
        REFERENCES utilisateurs.t_applications (id_application) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT temp_user_id_application_fkey FOREIGN KEY (id_organisme)
        REFERENCES utilisateurs.bib_organismes (id_organisme) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS utilisateurs.cor_role_token
(
    id_role INTEGER,
    token text
);

ALTER TABLE ONLY utilisateurs.cor_role_token ADD CONSTRAINT cor_role_token_pk_id_role PRIMARY KEY (id_role);

ALTER TABLE ONLY utilisateurs.cor_role_token ADD CONSTRAINT cor_role_token_fk_id_role FOREIGN KEY (id_role)
    REFERENCES utilisateurs.t_roles (id_role) MATCH SIMPLE
    ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE utilisateurs.t_roles
ADD COLUMN champs_addi jsonb;
