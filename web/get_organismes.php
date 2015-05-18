<?php 
	include "verification.php";
	$id=$_GET['id'];
	$form=$_GET['form'];
    $tab = array( CHR(13) => " ", CHR(10) => " " );
//si un organisme et un seul doit être retourné	
	if($id>0){
		$sqliste = "SELECT * FROM utilisateurs.bib_organismes
		WHERE id_organisme=$id";
	}
	else{
	$sqliste = "SELECT * FROM utilisateurs.bib_organismes";
	}
	$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
	$nb = pg_numrows($result);
		$json = "[";
		$i = 0;
		while ($val = pg_fetch_assoc($result)){
			$id_organisme = $val['id_organisme'];
			$nom_organisme = str_replace("'","\'",$val['nom_organisme']);
			$adresse_organisme = str_replace("'","\'",$val['adresse_organisme']);$adresse_organisme = strtr($adresse_organisme,$tab);		
            $cp_organisme = $val['cp_organisme'];
            $ville_organisme = str_replace("'","\'",$val['ville_organisme']);$ville_organisme = strtr($ville_organisme,$tab);
            $tel_organisme = $val['tel_organisme'];
            $fax_organisme = $val['fax_organisme'];
            $email_organisme = $val['email_organisme'];
			$text = "{id_organisme:".$id_organisme.",nom_organisme:'".$nom_organisme."',adresse_organisme:'".$adresse_organisme."',cp_organisme:'".$cp_organisme."',ville_organisme:'".$ville_organisme."',tel_organisme:'".$tel_organisme."',fax_organisme:'".$fax_organisme."',email_organisme:'".$email_organisme."'}";
            $json = $json.$text;
			$i++;
			if ($i > 0 and $i!=$nb) {
				$json = $json. ",";
			}
		}
		$json = $json."]";	
		
	if($form){
			echo "{success: true, data:{id_organisme:".$id_organisme.",nom_organisme:'".$nom_organisme."',adresse_organisme:'".$adresse_organisme.",cp_organisme:'".$cp_organisme.",ville_organisme:'".$ville_organisme.",tel_organisme:'".$tel_organisme.",fax_organisme:'".$fax_organisme.",email_organisme:'".$email_organisme."'}}";
		}
	else{
		echo $json;
	}
?>