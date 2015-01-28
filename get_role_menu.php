<?php 
include "verification.php";
$id_menu = $_GET['id_menu'];
$sqliste = "SELECT c.*, u.nom_role, u.prenom_role, b.nom_unite FROM utilisateurs.cor_role_menu c
			JOIN utilisateurs.t_roles u on u.id_role = c.id_role
			LEFT JOIN utilisateurs.bib_unites b ON b.id_unite = u.id_unite
			WHERE c.id_menu = $id_menu";
$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
$nb = pg_numrows($result);
$json = "[";
$i = 0;
while ($val = pg_fetch_assoc($result)){
	$id_role = $val['id_role'];
	$role = str_replace("'","\'",$val['nom_role']).' '.str_replace("'","\'",$val['prenom_role']);
	$nom_unite = str_replace("'","\'",$val['nom_unite']);
	$id_menu = $val['id_menu'];
	$text = "{id_role:".$id_role.",role:'".$role."',id_menu:".$id_menu.",nom_unite:'".$nom_unite."'}";
	$json = $json.$text;
	$i++;
	if ($i > 0 and $i!=$nb) {
		$json = $json. ",";
	}
}
$json = $json."]";	

echo $json;

?>

