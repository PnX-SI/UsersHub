--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.9
-- Dumped by pg_dump version 9.3.1
-- Started on 2015-01-26 14:11:24

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 9 (class 2615 OID 51956)
-- Name: utilisateurs; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA utilisateurs;

SET search_path = utilisateurs, pg_catalog;

--
-- TOC entry 1206 (class 1255 OID 52059)
-- Name: modify_date_insert(); Type: FUNCTION; Schema: utilisateurs; Owner: -
--

CREATE FUNCTION modify_date_insert() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.date_insert := now();
    NEW.date_update := now();
    RETURN NEW;
END;
$$;


--
-- TOC entry 1201 (class 1255 OID 52060)
-- Name: modify_date_update(); Type: FUNCTION; Schema: utilisateurs; Owner: -
--

CREATE FUNCTION modify_date_update() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.date_update := now();
    RETURN NEW;
END;
$$;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 216 (class 1259 OID 52225)
-- Name: cor_role_menu; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE cor_role_menu (
    id_role integer NOT NULL,
    id_menu integer NOT NULL
);


--
-- TOC entry 3546 (class 0 OID 0)
-- Dependencies: 216
-- Name: TABLE cor_role_menu; Type: COMMENT; Schema: utilisateurs; Owner: -
--

COMMENT ON TABLE cor_role_menu IS 'gestion du contenu des menus utilisateurs dans les applications';


--
-- TOC entry 217 (class 1259 OID 52228)
-- Name: cor_roles; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE cor_roles (
    id_role_groupe integer NOT NULL,
    id_role_utilisateur integer NOT NULL
);


--
-- TOC entry 218 (class 1259 OID 52231)
-- Name: t_roles_id_seq; Type: SEQUENCE; Schema: utilisateurs; Owner: -
--

CREATE SEQUENCE t_roles_id_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 219 (class 1259 OID 52233)
-- Name: t_roles; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE t_roles (
    groupe boolean DEFAULT false NOT NULL,
    id_role integer DEFAULT nextval('t_roles_id_seq'::regclass) NOT NULL,
    identifiant character varying(100),
    nom_role character varying(50),
    prenom_role character varying(50),
    desc_role text,
    pass character varying(100),
    email character varying(250),
    id_organisme integer,
    organisme character(32),
    id_unite integer,
    remarques text,
    pn boolean,
    session_appli character varying(50),
    date_insert timestamp without time zone,
    date_update timestamp without time zone
);


--
-- TOC entry 275 (class 1259 OID 52565)
-- Name: bib_organismes_id_seq; Type: SEQUENCE; Schema: utilisateurs; Owner: -
--

CREATE SEQUENCE bib_organismes_id_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 276 (class 1259 OID 52567)
-- Name: bib_organismes; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE bib_organismes (
    nom_organisme character varying(100) NOT NULL,
    adresse_organisme character varying(128),
    cp_organisme character varying(5),
    ville_organisme character varying(100),
    tel_organisme character varying(14),
    fax_organisme character varying(14),
    email_organisme character varying(100),
    id_organisme integer DEFAULT nextval('bib_organismes_id_seq'::regclass) NOT NULL
);


--
-- TOC entry 307 (class 1259 OID 52777)
-- Name: bib_droits; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE bib_droits (
    id_droit integer NOT NULL,
    nom_droit character varying(50),
    desc_droit text
);


--
-- TOC entry 308 (class 1259 OID 52783)
-- Name: bib_observateurs; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE bib_observateurs (
    codeobs character varying(6) NOT NULL,
    nom character varying(100),
    prenom character varying(100),
    orphelin integer
);


--
-- TOC entry 309 (class 1259 OID 52786)
-- Name: bib_unites_id_seq; Type: SEQUENCE; Schema: utilisateurs; Owner: -
--

CREATE SEQUENCE bib_unites_id_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 310 (class 1259 OID 52788)
-- Name: bib_unites; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE bib_unites (
    nom_unite character varying(50) NOT NULL,
    adresse_unite character varying(128),
    cp_unite character varying(5),
    ville_unite character varying(100),
    tel_unite character varying(14),
    fax_unite character varying(14),
    email_unite character varying(100),
    id_unite integer DEFAULT nextval('bib_unites_id_seq'::regclass) NOT NULL
);


--
-- TOC entry 311 (class 1259 OID 52792)
-- Name: cor_role_droit_application; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE cor_role_droit_application (
    id_role integer NOT NULL,
    id_droit integer NOT NULL,
    id_application integer NOT NULL
);


--
-- TOC entry 314 (class 1259 OID 52801)
-- Name: t_applications; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE t_applications (
    id_application integer NOT NULL,
    nom_application character varying(50) NOT NULL,
    desc_application text
);


--
-- TOC entry 315 (class 1259 OID 52807)
-- Name: t_applications_id_application_seq; Type: SEQUENCE; Schema: utilisateurs; Owner: -
--

CREATE SEQUENCE t_applications_id_application_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3547 (class 0 OID 0)
-- Dependencies: 315
-- Name: t_applications_id_application_seq; Type: SEQUENCE OWNED BY; Schema: utilisateurs; Owner: -
--

ALTER SEQUENCE t_applications_id_application_seq OWNED BY t_applications.id_application;


--
-- TOC entry 316 (class 1259 OID 52809)
-- Name: t_menus; Type: TABLE; Schema: utilisateurs; Owner: -; Tablespace: 
--

CREATE TABLE t_menus (
    id_menu integer NOT NULL,
    nom_menu character varying(50) NOT NULL,
    desc_menu text,
    id_application integer
);


--
-- TOC entry 3548 (class 0 OID 0)
-- Dependencies: 316
-- Name: TABLE t_menus; Type: COMMENT; Schema: utilisateurs; Owner: -
--

COMMENT ON TABLE t_menus IS 'table des menus déroulants des applications. Les roles de niveau groupes ou utilisateurs devant figurer dans un menu sont gérés dans la table cor_role_menu_application.';


--
-- TOC entry 317 (class 1259 OID 52815)
-- Name: t_menus_id_menu_seq; Type: SEQUENCE; Schema: utilisateurs; Owner: -
--

CREATE SEQUENCE t_menus_id_menu_seq
    START WITH 1000000
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3549 (class 0 OID 0)
-- Dependencies: 317
-- Name: t_menus_id_menu_seq; Type: SEQUENCE OWNED BY; Schema: utilisateurs; Owner: -
--

ALTER SEQUENCE t_menus_id_menu_seq OWNED BY t_menus.id_menu;

--
-- TOC entry 3367 (class 2604 OID 178256)
-- Name: id_application; Type: DEFAULT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY t_applications ALTER COLUMN id_application SET DEFAULT nextval('t_applications_id_application_seq'::regclass);


--
-- TOC entry 3368 (class 2604 OID 178257)
-- Name: id_menu; Type: DEFAULT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY t_menus ALTER COLUMN id_menu SET DEFAULT nextval('t_menus_id_menu_seq'::regclass);


--
-- TOC entry 3378 (class 2606 OID 53526)
-- Name: bib_droits_pkey; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY bib_droits
    ADD CONSTRAINT bib_droits_pkey PRIMARY KEY (id_droit);


--
-- TOC entry 3380 (class 2606 OID 53528)
-- Name: bib_observateurs_pk; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY bib_observateurs
    ADD CONSTRAINT bib_observateurs_pk PRIMARY KEY (codeobs);


--
-- TOC entry 3384 (class 2606 OID 53530)
-- Name: cor_role_droit_application_pkey; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cor_role_droit_application
    ADD CONSTRAINT cor_role_droit_application_pkey PRIMARY KEY (id_role, id_droit, id_application);


--
-- TOC entry 3370 (class 2606 OID 53533)
-- Name: cor_role_menu_pkey; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cor_role_menu
    ADD CONSTRAINT cor_role_menu_pkey PRIMARY KEY (id_role, id_menu);


--
-- TOC entry 3372 (class 2606 OID 53535)
-- Name: cor_roles_pkey; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cor_roles
    ADD CONSTRAINT cor_roles_pkey PRIMARY KEY (id_role_groupe, id_role_utilisateur);


--
-- TOC entry 3376 (class 2606 OID 53539)
-- Name: pk_bib_organismes; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY bib_organismes
    ADD CONSTRAINT pk_bib_organismes PRIMARY KEY (id_organisme);


--
-- TOC entry 3382 (class 2606 OID 53541)
-- Name: pk_bib_services; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY bib_unites
    ADD CONSTRAINT pk_bib_services PRIMARY KEY (id_unite);


--
-- TOC entry 3374 (class 2606 OID 53543)
-- Name: pk_roles; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY t_roles
    ADD CONSTRAINT pk_roles PRIMARY KEY (id_role);


--
-- TOC entry 3390 (class 2606 OID 53547)
-- Name: t_applications_pkey; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY t_applications
    ADD CONSTRAINT t_applications_pkey PRIMARY KEY (id_application);


--
-- TOC entry 3392 (class 2606 OID 53549)
-- Name: t_menus_pkey; Type: CONSTRAINT; Schema: utilisateurs; Owner: -; Tablespace: 
--

ALTER TABLE ONLY t_menus
    ADD CONSTRAINT t_menus_pkey PRIMARY KEY (id_menu);


--
-- TOC entry 3403 (class 2620 OID 53662)
-- Name: modify_date_insert_trigger; Type: TRIGGER; Schema: utilisateurs; Owner: -
--

CREATE TRIGGER modify_date_insert_trigger BEFORE INSERT ON t_roles FOR EACH ROW EXECUTE PROCEDURE modify_date_insert();


--
-- TOC entry 3404 (class 2620 OID 53663)
-- Name: modify_date_update_trigger; Type: TRIGGER; Schema: utilisateurs; Owner: -
--

CREATE TRIGGER modify_date_update_trigger BEFORE UPDATE ON t_roles FOR EACH ROW EXECUTE PROCEDURE modify_date_update();


--
-- TOC entry 3399 (class 2606 OID 54329)
-- Name: cor_role_droit_application_id_application_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY cor_role_droit_application
    ADD CONSTRAINT cor_role_droit_application_id_application_fkey FOREIGN KEY (id_application) REFERENCES t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3400 (class 2606 OID 54334)
-- Name: cor_role_droit_application_id_droit_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY cor_role_droit_application
    ADD CONSTRAINT cor_role_droit_application_id_droit_fkey FOREIGN KEY (id_droit) REFERENCES bib_droits(id_droit) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3401 (class 2606 OID 54339)
-- Name: cor_role_droit_application_id_role_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY cor_role_droit_application
    ADD CONSTRAINT cor_role_droit_application_id_role_fkey FOREIGN KEY (id_role) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3393 (class 2606 OID 54344)
-- Name: cor_role_menu_application_id_menu_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY cor_role_menu
    ADD CONSTRAINT cor_role_menu_application_id_menu_fkey FOREIGN KEY (id_menu) REFERENCES t_menus(id_menu) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3394 (class 2606 OID 54349)
-- Name: cor_role_menu_application_id_role_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY cor_role_menu
    ADD CONSTRAINT cor_role_menu_application_id_role_fkey FOREIGN KEY (id_role) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3395 (class 2606 OID 54354)
-- Name: cor_roles_id_role_groupe_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY cor_roles
    ADD CONSTRAINT cor_roles_id_role_groupe_fkey FOREIGN KEY (id_role_groupe) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3396 (class 2606 OID 54359)
-- Name: cor_roles_id_role_utilisateur_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY cor_roles
    ADD CONSTRAINT cor_roles_id_role_utilisateur_fkey FOREIGN KEY (id_role_utilisateur) REFERENCES t_roles(id_role) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3402 (class 2606 OID 54364)
-- Name: t_menus_id_application_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY t_menus
    ADD CONSTRAINT t_menus_id_application_fkey FOREIGN KEY (id_application) REFERENCES t_applications(id_application) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- TOC entry 3397 (class 2606 OID 54369)
-- Name: t_roles_id_organisme_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY t_roles
    ADD CONSTRAINT t_roles_id_organisme_fkey FOREIGN KEY (id_organisme) REFERENCES bib_organismes(id_organisme) ON UPDATE CASCADE;


--
-- TOC entry 3398 (class 2606 OID 54374)
-- Name: t_roles_id_unite_fkey; Type: FK CONSTRAINT; Schema: utilisateurs; Owner: -
--

ALTER TABLE ONLY t_roles
    ADD CONSTRAINT t_roles_id_unite_fkey FOREIGN KEY (id_unite) REFERENCES bib_unites(id_unite) ON UPDATE CASCADE;
    
SET search_path = utilisateurs, pg_catalog;
-- 
-- TOC entry 3274 (class 0 OID 17813)
-- Dependencies: 254
-- Data for Name: bib_droits; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 
INSERT INTO bib_droits (id_droit, nom_droit, desc_droit) VALUES (5, 'validateur', 'Il valide bien sur');
INSERT INTO bib_droits (id_droit, nom_droit, desc_droit) VALUES (4, 'modérateur', 'Peu utilisé');
INSERT INTO bib_droits (id_droit, nom_droit, desc_droit) VALUES (0, 'aucun', 'aucun droit.');
INSERT INTO bib_droits (id_droit, nom_droit, desc_droit) VALUES (1, 'utilisateur', 'Ne peut que consulter');
INSERT INTO bib_droits (id_droit, nom_droit, desc_droit) VALUES (2, 'rédacteur', 'Il possède des droit d''écriture pour créer des enregistrements');
INSERT INTO bib_droits (id_droit, nom_droit, desc_droit) VALUES (6, 'administrateur', 'Il a tous les droits');
INSERT INTO bib_droits (id_droit, nom_droit, desc_droit) VALUES (3, 'référent', 'utilisateur ayant des droits complémentaires au rédacteur (par exemple exporter des données ou autre)');
-- 
-- TOC entry 3275 (class 0 OID 17821)
-- Dependencies: 256
-- Data for Name: bib_organismes; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 
INSERT INTO bib_organismes (nom_organisme, adresse_organisme, cp_organisme, ville_organisme, tel_organisme, fax_organisme, email_organisme, id_organisme) VALUES ('PNF', NULL, NULL, 'Montpellier', NULL, NULL, NULL, 1);
INSERT INTO bib_organismes (nom_organisme, adresse_organisme, cp_organisme, ville_organisme, tel_organisme, fax_organisme, email_organisme, id_organisme) VALUES ('Parc National des Ecrins', 'Domaine de Charance', '05000', 'GAP', '04 92 40 20 10', '', '', 2);
INSERT INTO bib_organismes (nom_organisme, adresse_organisme, cp_organisme, ville_organisme, tel_organisme, fax_organisme, email_organisme, id_organisme) VALUES ('Autre', '', '', '', '', '', '', 99);
-- 
-- TOC entry 3276 (class 0 OID 17827)
-- Dependencies: 258
-- Data for Name: bib_unites; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 

INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Virtuel', NULL, NULL, NULL, NULL, NULL, NULL, 1);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('personnels partis', NULL, NULL, NULL, NULL, NULL, NULL, 2);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Stagiaires', NULL, NULL, '', '', NULL, NULL, 3);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Secretariat général', '', '', '', '', NULL, NULL, 4);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Service scientifique', '', '', '', '', NULL, NULL, 5);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Service SI', '', '', '', '', NULL, NULL, 6);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Service Communication', '', '', '', '', NULL, NULL, 7);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Conseil scientifique', '', '', '', NULL, NULL, NULL, 8);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Conseil d''administration', '', '', '', NULL, NULL, NULL, 9);
INSERT INTO bib_unites (nom_unite, adresse_unite, cp_unite, ville_unite, tel_unite, fax_unite, email_unite, id_unite) VALUES ('Autres', NULL, NULL, NULL, NULL, NULL, NULL, 99);
-- 
-- TOC entry 3278 (class 0 OID 17837)
-- Dependencies: 261
-- Data for Name: t_applications; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 
INSERT INTO t_applications (id_application, nom_application, desc_application) VALUES (1, 'application utilisateurs', 'application permettant d''administrer la présente base de données.');
INSERT INTO t_applications (id_application, nom_application, desc_application) VALUES (14, 'application geonature', 'Application permettant la consultation et la gestion des relevés faune et flore.');

-- 
-- TOC entry 3255 (class 0 OID 17445)
-- Dependencies: 189
-- Data for Name: t_roles; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, organisme, id_unite, pn, session_appli, date_insert, date_update, id_organisme, remarques) VALUES (true, 20002, NULL, 'grp_en_poste', NULL, 'Tous les agents en poste au PN', NULL, NULL, 'monpn', 99, true, NULL, NULL, NULL, NULL,'groupe test');
INSERT INTO t_roles (groupe, id_role, identifiant, nom_role, prenom_role, desc_role, pass, email, organisme, id_unite, pn, session_appli, date_insert, date_update, id_organisme, remarques) VALUES (false, 1, 'admin', 'Administrateur', 'test', NULL, '21232f297a57a5a743894a0e4a801fc3', '', 'Parc national des Ecrins', 1, true, NULL, NULL, NULL, 99,'utilisateur test à modifier');
-- 
-- TOC entry 3277 (class 0 OID 17831)
-- Dependencies: 259
-- Data for Name: cor_role_droit_application; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 
INSERT INTO cor_role_droit_application (id_role, id_droit, id_application) VALUES (1, 6, 1);
INSERT INTO cor_role_droit_application (id_role, id_droit, id_application) VALUES (20002, 3, 14);
INSERT INTO cor_role_droit_application (id_role, id_droit, id_application) VALUES (1, 6, 14);
-- 
-- TOC entry 3279 (class 0 OID 17845)
-- Dependencies: 263
-- Data for Name: t_menus; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 
INSERT INTO t_menus (id_menu, nom_menu, desc_menu, id_application) VALUES (9, 'faune - Observateurs', 'listes des observateurs faune', 14);
INSERT INTO t_menus (id_menu, nom_menu, desc_menu, id_application) VALUES (10, 'flore - Observateurs', 'Liste des observateurs flore', 14);
-- 
-- TOC entry 3253 (class 0 OID 17437)
-- Dependencies: 186
-- Data for Name: cor_role_menu; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 
INSERT INTO cor_role_menu (id_role, id_menu) VALUES (1, 10);
INSERT INTO cor_role_menu (id_role, id_menu) VALUES (1, 9);
-- 
-- TOC entry 3254 (class 0 OID 17440)
-- Dependencies: 187
-- Data for Name: cor_roles; Type: TABLE DATA; Schema: utilisateurs; Owner: geonatuser
-- 
INSERT INTO cor_roles (id_role_groupe, id_role_utilisateur) VALUES (20002, 1);


-- Completed on 2015-01-26 14:11:48

--
-- PostgreSQL database dump complete
--

