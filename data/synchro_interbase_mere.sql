-- SUR LA BASE MERE
CREATE EXTENSION IF NOT EXISTS dblink;

-- DROP TABLE utilisateurs.t_synchro_logs CASCADE;
CREATE TABLE utilisateurs.t_synchro_logs (
	id serial PRIMARY KEY,
	date_op timestamp DEFAULT (now()),
	operation varchar(250),
	table_name varchar(250) NOT NULL,
	table_cor boolean NOT NULL,
	id_name varchar(250),
	id_object int,
    archive boolean DEFAULT (FALSE)
);

-- DROP TABLE utilisateurs.t_synchro_databases CASCADE;
CREATE TABLE utilisateurs.t_synchro_databases (
	id serial PRIMARY KEY,
	host varchar(250),
	port int,
	dbname varchar(250),
	"user" varchar(250),
	"password" varchar(250)
);


CREATE TABLE utilisateurs.t_synchro_databases_logs_done
(
  id_database integer,
  id_log integer,
  success boolean DEFAULT false,
  CONSTRAINT t_synchro_databases_logs_done_id_database_fkey FOREIGN KEY (id_database)
      REFERENCES utilisateurs.t_synchro_databases (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT t_synchro_databases_logs_done_id_log_fkey FOREIGN KEY (id_log)
      REFERENCES utilisateurs.t_synchro_logs (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE CASCADE,
  CONSTRAINT t_synchro_databases_logs_done_pkey PRIMARY KEY (id_database, id_log)
);


CREATE OR REPLACE FUNCTION utilisateurs.fct_trg_log_actions_per_db()
  RETURNS trigger AS
$BODY$
DECLARE
BEGIN

    INSERT INTO utilisateurs.t_synchro_databases_logs_done (id_database, id_log, success)
    SELECT id, NEW.id, FALSE
    FROM utilisateurs.t_synchro_databases;

    RETURN NULL;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;


CREATE TRIGGER trg_utilisateurs_log_actions_per_db
  AFTER INSERT
  ON utilisateurs.t_synchro_logs
  FOR EACH ROW
  EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions_per_db();


CREATE OR REPLACE FUNCTION utilisateurs.synchro_child_db()
  RETURNS boolean AS
$BODY$
  DECLARE
    actions RECORD;
    db RECORD;
    e_sql TEXT;
    _db_conn text;
  BEGIN

  -- Suppression des doublons de logs
	DELETE
	FROM utilisateurs.t_synchro_logs  a
	USING utilisateurs.t_synchro_logs  b
	WHERE
	    a.id > b.id
	    AND ((a.operation = b.operation AND a.id_name = b.id_name AND a.id_object = b.id_object) OR a.table_cor = true)
	    AND a.table_name = b.table_name
	    AND a.archive = false and b.archive = false;


	-- Construction de la requete en fonction des actions à réaliser pour chaque base
	FOR db IN (SELECT * FROM  utilisateurs.t_synchro_databases) LOOP
		BEGIN

			-- Test de connexion à la base
			_db_conn := 'dbname='|| db.dbname ||' port='|| db.port ||' host='|| db.host ||' user='|| db.user ||' password='|| db.password;
			RAISE NOTICE '%', _db_conn;
			IF (SELECT * FROM dblink(_db_conn, 'SELECT 1 as id' ) AS t (id int)) = 1 THEN


				FOR actions IN (
					SELECT l.*
					FROM  utilisateurs.t_synchro_logs l
					JOIN utilisateurs.t_synchro_databases_logs_done d ON d.id_log = l.id
					WHERE d.id_database = db.id AND success = False ORDER BY date_op
				) LOOP
					RAISE NOTICE '%', actions.operation;
					IF actions.table_cor = TRUE THEN
						e_sql := 'TRUNCATE TABLE utilisateurs.'||actions.table_name||';  INSERT INTO utilisateurs.'||actions.table_name||' SELECT * FROM fdw_utilisateurs.'||actions.table_name;
					ELSIF actions.operation = 'UPDATE' THEN
						SELECT INTO e_sql 'UPDATE utilisateurs.'||actions.table_name||' u SET '|| string_agg(column_name || ' = a.' || column_name , ','  )||
							' FROM fdw_utilisateurs.'||actions.table_name||' as a WHERE a.' || actions.id_name || ' = u.' || actions.id_name || ' AND  a.'|| actions.id_name || ' = ' ||  actions.id_object
						FROM information_schema.columns WHERE table_schema = 'utilisateurs' AND table_name = actions.table_name
						GROUP BY table_schema, table_name;
					ELSIF actions.operation = 'INSERT' THEN
						e_sql :=  'INSERT INTO utilisateurs.'||actions.table_name||' SELECT * FROM fdw_utilisateurs.'||actions.table_name||' as a WHERE a.' || actions.id_name || ' = ' || actions.id_object;
					ELSIF actions.operation = 'DELETE' THEN
						e_sql := 'DELETE FROM utilisateurs.'||actions.table_name||' WHERE ' || actions.id_name || ' = ' || actions.id_object;
					END IF;
					-- Lancement des actions sur les bases filles
					RAISE NOTICE '%', e_sql;
					BEGIN
						PERFORM dblink_exec(_db_conn , e_sql);

						UPDATE utilisateurs.t_synchro_databases_logs_done SET success = true
						WHERE id_database = db.id AND id_log = actions.id;

					exception WHEN others THEN
					    RAISE notice 'ERROR % %', SQLERRM, SQLSTATE;
					END;
				END LOOP;
			END IF;
		exception WHEN others THEN
		    RAISE notice 'ERROR % %', SQLERRM, SQLSTATE;
		END;
	END LOOP;

	-- Mise en archives des opérations réalisées sur l'ensemble des bases déclarées
	UPDATE utilisateurs.t_synchro_logs SET archive = TRUE
	FROM (
		SELECT count(DISTINCT id_database) - count(DISTINCT id_database) FILTER (WHERE success = TRUE) as nb, id_log
		FROM utilisateurs.t_synchro_databases_logs_done
		GROUP BY id_log
	) a
	WHERE nb = 0 AND id = id_log;

    RETURN TRUE;
  END;
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;


--Trigger permettant le log des actions
CREATE OR REPLACE FUNCTION utilisateurs.fct_trg_log_actions()
  RETURNS trigger AS
$BODY$
DECLARE
   _id_object int;
BEGIN
    IF TG_ARGV[0]::boolean = TRUE THEN
	    _id_object := NULL;
    ELSIF TG_OP = 'DELETE' THEN
	    EXECUTE format('SELECT ($1).%s::text', TG_ARGV[1])
	    USING OLD
	    INTO  _id_object;
    ELSE
	EXECUTE format('SELECT ($1).%s::text', TG_ARGV[1])
	    USING NEW
	    INTO  _id_object;
    END IF;

    INSERT INTO utilisateurs.t_synchro_logs (operation, table_name, table_cor, id_name, id_object)
    SELECT TG_OP, TG_TABLE_NAME, TG_ARGV[0]::boolean, TG_ARGV[1], _id_object;

    return NULL;
END;
$BODY$
  LANGUAGE plpgsql VOLATILE;


-- Triggers sur l'ensemble des tables du schéma utilisateurs
do $$
begin
CREATE TRIGGER trg_utilisateurs_bib_droits_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.bib_droits
          for each row
 execute procedure utilisateurs.fct_trg_log_actions(False, 'id_droit');
exception when others then
    raise notice '% %', SQLERRM, SQLSTATE;
end;
$$ language 'plpgsql';

CREATE TRIGGER trg_utilisateurs_bib_organismes_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.bib_organismes
          for each row
 execute procedure utilisateurs.fct_trg_log_actions(False, 'id_organisme');

CREATE TRIGGER trg_utilisateurs_bib_tag_types_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.bib_tag_types
          for each row
 execute procedure utilisateurs.fct_trg_log_actions(False, 'id_tag_type');

CREATE TRIGGER trg_utilisateurs_bib_unites_types_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.bib_unites
          for each row
 execute procedure utilisateurs.fct_trg_log_actions(False, 'id_unite');

CREATE TRIGGER trg_utilisateurs_cor_tags_relations_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.cor_tags_relations
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(TRUE, 'none');

CREATE TRIGGER trg_utilisateurs_cor_organism_tag_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.cor_organism_tag
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(TRUE, 'none');

CREATE TRIGGER trg_utilisateurs_cor_role_tag_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.cor_role_tag
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(TRUE, 'none');

do $$
begin
CREATE TRIGGER trg_utilisateurs_cor_role_droit_application_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.cor_role_droit_application
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(TRUE, 'none');

exception when others then
    raise notice '% %', SQLERRM, SQLSTATE;
end;
$$ language 'plpgsql';

do $$
begin
CREATE TRIGGER trg_utilisateurs_cor_role_menu_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.cor_role_menu
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(TRUE, 'none');

exception when others then
    raise notice '% %', SQLERRM, SQLSTATE;
end;
$$ language 'plpgsql';

CREATE TRIGGER trg_utilisateurs_cor_roles_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.cor_roles
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(TRUE, 'none');

CREATE TRIGGER trg_utilisateurs_cor_application_tag_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.cor_application_tag
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(TRUE, 'none');

CREATE TRIGGER trg_utilisateurs_cor_app_privileges_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.cor_app_privileges
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(TRUE, 'none');

do $$
begin
CREATE TRIGGER trg_utilisateurs_t_menus_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.t_menus
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(FALSE, 'id_menu');

exception when others then
    raise notice '% %', SQLERRM, SQLSTATE;
end;
$$ language 'plpgsql';

CREATE TRIGGER trg_utilisateurs_t_applications_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.t_applications
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(FALSE, 'id_application');

CREATE TRIGGER trg_utilisateurs_t_tags_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.t_tags
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(FALSE, 'id_tag');

CREATE TRIGGER trg_utilisateurs_t_roles_log_a
     AFTER INSERT OR UPDATE OR DELETE on utilisateurs.t_roles
          FOR EACH ROW
 EXECUTE PROCEDURE utilisateurs.fct_trg_log_actions(FALSE, 'id_role');

