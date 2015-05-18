<?php 
	include "verification.php";
	$id=$_GET['id'];
	$form=$_GET['form'];
    $tab = array( CHR(13) => " ", CHR(10) => " " );
//si un droit et un seul doit être retourné	
	if($id>0){
		$sqliste = "SELECT * FROM utilisateurs.bib_droits
		WHERE id_droit=$id";
	}
	else{
	$sqliste = "SELECT * FROM utilisateurs.bib_droits";
	}
	$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
	$nb = pg_numrows($result);
		$json = "[";
		$i = 0;
		while ($val = pg_fetch_assoc($result)){
			$id_droit = $val['id_droit'];
			$nom_droit = str_replace("'","\'",$val['nom_droit']);
			$desc_droit = str_replace("'","\'",$val['desc_droit']);$desc_droit = strtr($desc_droit,$tab);
			$text = "{id_droit:".$id_droit.",nom_droit:'".$nom_droit."',desc_droit:'".$desc_droit."'}";
			$json = $json.$text;
			$i++;
			if ($i > 0 and $i!=$nb) {
				$json = $json. ",";
			}
		}
		$json = $json."]";	
		
	if($form){
			echo "{success: true, data:{id_droit:".$id_droit.",nom_droit:'".$nom_droit."',desc_droit:'".$desc_droit."'}}";
		}
	else{
		echo $json;
	}
?>

