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