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
    password_confirmation text,
    email character varying(250),
    id_organisme integer,
    organisme character(32),
    remarques text,
    pn boolean,
    session_appli character varying(50),
    date_insert timestamp without time zone,
    date_update timestamp without time zone,

    CONSTRAINT pk_temp_users     PRIMARY KEY (id_temp_user),

    CONSTRAINT t_roles_id_organisme_fkey FOREIGN KEY (id_organisme)
        REFERENCES utilisateurs.bib_organismes (id_organisme) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE
);

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
    password_confirmation text,
    email character varying(250),
    id_organisme integer,
    organisme character(32),
    remarques text,
    pn boolean,
    session_appli character varying(50),
    date_insert timestamp without time zone,
    date_update timestamp without time zone,

    CONSTRAINT pk_temp_users     PRIMARY KEY (id_temp_user),

    CONSTRAINT t_roles_id_organisme_fkey FOREIGN KEY (id_organisme)
        REFERENCES utilisateurs.bib_organismes (id_organisme) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE
);