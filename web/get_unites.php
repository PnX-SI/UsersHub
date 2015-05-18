<?php 
	include "verification.php";
	$id=$_GET['id'];
	$form=$_GET['form'];
    $tab = array( CHR(13) => " ", CHR(10) => " " );
//si un unite et un seul doit être retourné	
	if($id>0){
		$sqliste = "SELECT * FROM utilisateurs.bib_unites
		WHERE id_unite=$id";
	}
	else{
	$sqliste = "SELECT * FROM utilisateurs.bib_unites";
	}
	$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
	$nb = pg_numrows($result);
		$json = "[";
		$i = 0;
		while ($val = pg_fetch_assoc($result)){
			$id_unite = $val['id_unite'];
			$nom_unite = str_replace("'","\'",$val['nom_unite']);
			$adresse_unite = str_replace("'","\'",$val['adresse_unite']);$adresse_unite = strtr($adresse_unite,$tab);		
            $cp_unite = $val['cp_unite'];
            $ville_unite = str_replace("'","\'",$val['ville_unite']);$ville_unite = strtr($ville_unite,$tab);
            $tel_unite = $val['tel_unite'];
            $fax_unite = $val['fax_unite'];
            $email_unite = $val['email_unite'];
			$text = "{id_unite:".$id_unite.",nom_unite:'".$nom_unite."',adresse_unite:'".$adresse_unite."',cp_unite:'".$cp_unite."',ville_unite:'".$ville_unite."',tel_unite:'".$tel_unite."',fax_unite:'".$fax_unite."',email_unite:'".$email_unite."'}";
			$json = $json.$text;
			$i++;
			if ($i > 0 and $i!=$nb) {
				$json = $json. ",";
			}
		}
		$json = $json."]";	
		
	if($form){
			echo "{success: true, data:{id_unite:".$id_unite.",nom_unite:'".$nom_unite."',adresse_unite:'".$adresse_unite.",cp_unite:'".$cp_unite.",ville_unite:'".$ville_unite.",tel_unite:'".$tel_unite.",fax_unite:'".$fax_unite.",email_unite:'".$email_unite."'}}";
		}
	else{
		echo $json;
	}
?>