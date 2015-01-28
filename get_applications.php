<?php 
	include "verification.php";
    $tab = array( CHR(13) => " ", CHR(10) => " " );
    
	$sqliste = "SELECT * FROM utilisateurs.t_applications WHERE id_application <> 1;";
	$result = pg_query($sqliste) or die ('Échec requête : ' . pg_last_error()) ;
	$nb = pg_numrows($result);
		$json = "[";
		$i = 0;
		while ($val = pg_fetch_assoc($result)){
			$id_application = $val['id_application'];
			$nom_application = str_replace("'","\'",$val['nom_application']);
			$desc_application = str_replace("'","\'",$val['desc_application']);$desc_application = strtr($desc_application,$tab);
			$connect_host = $val['connect_host'];
			$connect_database = $val['connect_database'];
			$connect_user = $val['connect_user'];
			$connect_pass = $val['connect_pass'];
			$text = "{id_application:".$id_application.",nom_application:'".$nom_application."',desc_application:'".$desc_application."',connect_host:'".$connect_host."',connect_database:'".$connect_database."',connect_user:'".$connect_user."',connect_pass:'".$connect_pass."'}";
			$json = $json.$text;
			$i++;
			if ($i > 0 and $i!=$nb) {
				$json = $json. ",";
			}
		}
		$json = $json."]";	

	echo $json;

?>

