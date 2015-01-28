<?php 
	include "verification.php";
    $tab = array( CHR(13) => " ", CHR(10) => " " );
    
	$sqliste = "SELECT * FROM utilisateurs.t_roles WHERE groupe = true";
	$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
	$nb = pg_numrows($result);
		$json = "[";
		$i = 0;
		while ($val = pg_fetch_assoc($result)){
			$id_groupe = $val['id_role'];
			$nom_groupe = str_replace("'","\'",$val['nom_role']);
			$desc_groupe = str_replace("'","\'",$val['desc_role']);$desc_groupe = strtr($desc_groupe,$tab);
			$text = "{id_groupe:".$id_groupe.",nom_groupe:'".$nom_groupe."',desc_groupe:'".$desc_groupe."'}";
			$json = $json.$text;
			$i++;
			if ($i > 0 and $i!=$nb) {
				$json = $json. ",";
			}
		}
		$json = $json."]";	

	echo $json;

?>

