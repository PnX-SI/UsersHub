<?php
session_start();
require("../config/connecter.php");
//requete permettant d'extraire l'utilisateur avec son niveau de droit maximum qu'il soit dans un role-groupe et/ou en tant qu'utilisateur seul 
$requete = "SELECT a.id_role, a.nom_role, a.prenom_role,max(a.id_droit) as id_droit, a.id_application 
FROM (
	(SELECT u.id_role, u.nom_role, u.prenom_role, c.id_droit, c.id_application
	FROM utilisateurs.t_roles u
	JOIN utilisateurs.cor_role_droit_application c ON c.id_role = u.id_role
	WHERE u.identifiant = '".$_SESSION['xlogin']."' AND u.session_appli = '".session_id()."' AND c.id_application = 1)
	union
	(SELECT g.id_role_utilisateur, u.nom_role, u.prenom_role, c.id_droit, c.id_application
	FROM utilisateurs.t_roles u
	JOIN utilisateurs.cor_roles g ON g.id_role_utilisateur = u.id_role
	JOIN utilisateurs.cor_role_droit_application c ON c.id_role = g.id_role_groupe
	WHERE u.identifiant = '".$_SESSION['xlogin']."' AND u.session_appli = '".session_id()."' AND c.id_application = 1)
) as a
GROUP BY a.id_role, a.nom_role, a.prenom_role,a.id_application
LIMIT 1";
$result = pg_query($requete) or die ("Erreur requête") ;
$verif = pg_numrows($result);

if ($verif != "1"){
	//redirection vers la page d'accueil
	header("Location: index.php");
}
else{
	while ($val = pg_fetch_assoc($result)){
		$id_droit = $val['id_droit'];
		$id_unite = $val['id_unite'];
		$nom_role = $val['nom_role'];
		$prenom_role = $val['prenom_role'];
		$id_user = $val['id_role'];
	}
}
?>
