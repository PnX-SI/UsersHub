DROP TABLE IF EXISTS utilisateurs.cor_role_token;

CREATE TABLE IF NOT EXISTS utilisateurs.cor_role_token
(

    id_role INTEGER,
    token text,

    CONSTRAINT cor_role_token_pk_id_role PRIMARY KEY (id_role),

    CONSTRAINT cor_role_token_fk_id_role FOREIGN KEY (id_role)
        REFERENCES utilisateurs.t_roles (id_role) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE

);

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
    id_unite integer,
    remarques text,
    pn boolean,
    session_appli character varying(50),
    date_insert timestamp without time zone,
    date_update timestamp without time zone,

    CONSTRAINT pk_temp_users     PRIMARY KEY (id_temp_user),

    CONSTRAINT t_roles_id_organisme_fkey FOREIGN KEY (id_organisme)
        REFERENCES utilisateurs.bib_organismes (id_organisme) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT t_roles_id_unite_fkey FOREIGN KEY (id_unite)
        REFERENCES utilisateurs.bib_unites (id_unite) MATCH SIMPLE
        ON UPDATE CASCADE ON DELETE CASCADE
);

DROP TRIGGER IF EXISTS tri_modify_date_insert_temp_roles ON utilisateurs.temp_users;

CREATE TRIGGER tri_modify_date_insert_temp_roles
    BEFORE INSERT
    ON utilisateurs.temp_users
    FOR EACH ROW
    EXECUTE PROCEDURE utilisateurs.modify_date_insert();
