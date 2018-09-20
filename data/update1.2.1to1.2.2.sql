DO
$$
BEGIN
CREATE OR REPLACE VIEW utilisateurs.v_userslist_forall_menu AS
 SELECT a.groupe,
    a.id_role,
    a.identifiant,
    a.nom_role,
    a.prenom_role,
    (upper(a.nom_role::text) || ' '::text) || a.prenom_role::text AS nom_complet,
    a.desc_role,
    a.pass,
    a.email,
    a.id_organisme,
    a.organisme,
    a.id_unite,
    a.remarques,
    a.pn,
    a.session_appli,
    a.date_insert,
    a.date_update,
    a.id_menu
   FROM ( SELECT u.groupe,
            u.id_role,
            u.identifiant,
            u.nom_role,
            u.prenom_role,
            u.desc_role,
            u.pass,
            u.email,
            u.id_organisme,
            u.organisme,
            u.id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_menu
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_role_menu c ON c.id_role = u.id_role
          WHERE u.groupe = false
        UNION
         SELECT u.groupe,
            u.id_role,
            u.identifiant,
            u.nom_role,
            u.prenom_role,
            u.desc_role,
            u.pass,
            u.email,
            u.id_organisme,
            u.organisme,
            u.id_unite,
            u.remarques,
            u.pn,
            u.session_appli,
            u.date_insert,
            u.date_update,
            c.id_menu
           FROM utilisateurs.t_roles u
             JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role
             JOIN utilisateurs.cor_role_menu c ON c.id_role = g.id_role_groupe
          WHERE u.groupe = false) a;
    EXCEPTION WHEN duplicate_object  THEN
    -- do nothing, it's already there
END
$$;