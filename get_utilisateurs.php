<?php 
include "verification.php";
function bool_to_oui_non($val){
    if ($val == 't'){$valeur = 'oui';}
    elseif ($val == 'f'){$valeur = 'non';}
    else{$valeur = null;}
    return $valeur;
}
$id_groupe = $_GET['id_groupe'];
$id_menu = $_GET['id_menu'];
$id_application= $_GET['id_application'];
$mon_groupe = $_GET['mon_groupe'];
$panel = $_GET['panel'];
$role = $_GET['role'];

if (isset($mon_groupe)){
	$sqliste = "SELECT u.id_role, u.nom_role, u.prenom_role, c.id_role_groupe, b.nom_unite, o.nom_organisme FROM utilisateurs.cor_roles c 
				JOIN utilisateurs.t_roles u ON u.id_role = c.id_role_utilisateur
				JOIN utilisateurs.bib_unites b ON b.id_unite = u.id_unite
				LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
				WHERE c.id_role_groupe = $mon_groupe
				AND u.groupe = false";
	$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
	$nb = pg_numrows($result);
	$json = "[";
	$i = 0;
	while ($val = pg_fetch_assoc($result)){
		$id_role = $val['id_role'];
		$role = str_replace("'","\'",$val['nom_role'])." ".str_replace("'","\'",$val['prenom_role']);
		$nom_unite = str_replace("'","\'",$val['nom_unite']);
		$nom_organisme = str_replace("'","\'",$val['nom_organisme']);
		$text = "{id_role:".$id_role.",role:'".$role."',nom_unite:'".$nom_unite."',nom_organisme:'".$nom_organisme."'}";
		$json = $json.$text;
		$i++;
		if ($i > 0 and $i!=$nb) {
			$json = $json. ",";
		}
	}
	$json = $json."]";	
	echo $json;
}
else{
	if ($role=='tous'){
		switch ($panel){
			case 'groupe':
				$sqliste = "SELECT u.*,b.nom_unite,o.nom_organisme FROM utilisateurs.t_roles u 
							LEFT JOIN utilisateurs.bib_unites b ON b.id_unite = u.id_unite 
                            LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme 
							WHERE u.id_role not in (SELECT id_role_utilisateur FROM utilisateurs.cor_roles where id_role_groupe = $id_groupe)";
				break;
			case 'menu':
				$sqliste = "SELECT u.*,b.nom_unite,o.nom_organisme FROM utilisateurs.t_roles u 
							LEFT JOIN utilisateurs.bib_unites b ON b.id_unite = u.id_unite 
                            LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme 
							WHERE u.id_role not in (SELECT id_role FROM utilisateurs.cor_role_menu where id_menu = $id_menu)";
				break;
			case 'application':
				$sqliste = "SELECT u.*,b.nom_unite,o.nom_organisme FROM utilisateurs.t_roles u 
							LEFT JOIN utilisateurs.bib_unites b ON b.id_unite = u.id_unite 
                            LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme 
							WHERE u.id_role not in (SELECT id_role FROM utilisateurs.cor_role_droit_application where id_application = $id_application)";
				break;
			default:
				$sqliste = "SELECT u.*,b.nom_unite,o.nom_organisme FROM utilisateurs.t_roles u 
							LEFT JOIN utilisateurs.bib_unites b ON b.id_unite = u.id_unite 
                            LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme";
		}
		$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
		$nb = pg_numrows($result);
		$json = "[";
		$i = 0;
		while ($val = pg_fetch_assoc($result)){
			$id_role = $val['id_role'];
			$role = str_replace("'","\'",$val['nom_role'])." ".str_replace("'","\'",$val['prenom_role']);
			$nom_unite = str_replace("'","\'",$val['nom_unite']);
			$nom_organisme = str_replace("'","\'",$val['nom_organisme']);
			$groupe = $val['groupe'];
			$text = "{id_role:".$id_role.",role:'".$role."',nom_unite:'".$nom_unite."',nom_organisme:'".$nom_organisme."',groupe:'".$groupe."'}";
			$json = $json.$text;
			$i++;
			if ($i > 0 and $i!=$nb) {
				$json = $json. ",";
			}
		}
		$json = $json."]";	
		echo $json;
	}
	else{
		$sqliste = "SELECT u.*, b.nom_unite,o.nom_organisme FROM utilisateurs.t_roles u 
				LEFT JOIN utilisateurs.bib_unites b ON b.id_unite = u.id_unite
                LEFT JOIN utilisateurs.bib_organismes o ON o.id_organisme = u.id_organisme
				WHERE u.groupe = false";
		$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
		$nb = pg_numrows($result);
		$json = "[";
		$i = 0;
		while ($val = pg_fetch_assoc($result)){
			$id_role = $val['id_role'];
			$role = str_replace("'","\'",$val['nom_role'])." ".str_replace("'","\'",$val['prenom_role']);
			$nom_role = str_replace("'","\'",$val['nom_role']);
			$prenom_role = str_replace("'","\'",$val['prenom_role']);
			$id_unite = $val['id_unite'];
			if($val['id_organisme']){$id_organisme = $val['id_organisme'];}else{$id_organisme = 2;}
			$nom_unite = str_replace("'","\'",$val['nom_unite']);
			$nom_organisme = str_replace("'","\'",$val['nom_organisme']);
			$remarques = str_replace( array( "'",CHR(10), CHR(13), "\n", "\r" ), array( "\'",' - ',' - ',' - ',' - '), $val['remarques'] );
			$email = $val['email'];
			$identifiant = $val['identifiant'];
			if($val['pass']!=null){
			$pass = "oui";
			}else{
			$pass = "non";
			}
			$pn = bool_to_oui_non($val['pn']);
			$text = "{id_role:".$id_role.",role:'".$role."',nom_role:'".$nom_role."',nom_organisme:'".$nom_organisme."',prenom_role:'".$prenom_role."',id_unite:".$id_unite.",nom_unite:'".$nom_unite."',id_organisme:".$id_organisme.",email:'".$email."',identifiant:'".$identifiant."',pass:'".$pass."',pn:'".$pn."',remarques:'".$remarques."'}";
			$json = $json.$text;
			$i++;
			if ($i > 0 and $i!=$nb) {
				$json = $json. ",";
			}
		}
		$json = $json."]";	
		echo $json;
	}
}
?>

