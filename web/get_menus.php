<?php 
	include "verification.php";
	$id=$_GET['id'];
	$form=$_GET['form'];
    $tab = array( CHR(13) => " ", CHR(10) => " " );
//si un menu et un seul doit être retourné	
	if($id>0){
		$sqliste = "SELECT * FROM utilisateurs.t_menus
		WHERE id_menu=$id";
	}
	else{
	$sqliste = "SELECT * FROM utilisateurs.t_menus";
	}
	$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
	$nb = pg_numrows($result);
		$json = "[";
		$i = 0;
		while ($val = pg_fetch_assoc($result)){
			$id_menu = $val['id_menu'];
			$nom_menu = str_replace("'","\'",$val['nom_menu']);
			$desc_menu = str_replace("'","\'",$val['desc_menu']);$desc_menu = strtr($desc_menu,$tab);
			$id_application = $val['id_application'];
			$text = "{id_menu:".$id_menu.",nom_menu:'".$nom_menu."',desc_menu:'".$desc_menu."',id_application:".$id_application."}";
			$json = $json.$text;
			$i++;
			if ($i > 0 and $i!=$nb) {
				$json = $json. ",";
			}
		}
		$json = $json."]";	
		
	if($form){
			echo "{success: true, data:{id_menu:".$id_menu.",nom_menu:'".$nom_menu."',desc_menu:'".$desc_menu."',id_application:".$id_application."}}";
		}
	else{
		echo $json;
	}
?>

