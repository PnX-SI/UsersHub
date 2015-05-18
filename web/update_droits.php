<?php
include "verification.php";
$id_droit =  $_GET['id_droit'];
//correction des magic_quotes_gpc (protection des chaînes de caractères)
$nom_droit = pg_escape_string($_GET['nom_droit']);
$desc_droit = pg_escape_string($_GET['desc_droit']);
$action = $_GET['action'];
//-----------création des connections pour mise à jour sur les différentes bases du fichier dbconnexions.json------------
$fp = fopen ("../config/dbconnexions.json", "r");
$contenu_du_fichier = fread ($fp, filesize('../config/dbconnexions.json'));
fclose ($fp);
$json = json_decode($contenu_du_fichier,true);
foreach ($json as $array) {
    foreach ($array as $database) {
        $db_fun_name = str_replace("'","\'",$database['dbfunname']);
        $connect_host = $database['host'];
        $connect_dbname = $database['dbname'];
        $connect_user = $database['user'];
        $connect_pass = $database['pass'];
        //connexion sur chacune des bases 
		if ($connect_host<>"" OR $connect_dbname<>"" OR $connect_user<>"" OR $connect_pass<>"") {
			$dbconn = pg_connect("host=$connect_host dbname=$connect_dbname user=$connect_user password=$connect_pass");
			if($action=="update"){ //Update d'un droit existant
				$sql = "Update utilisateurs.bib_droits 
				set id_droit = '$id_droit', 
				nom_droit = '$nom_droit',
				desc_droit = '$desc_droit'
				WHERE id_droit = $id_droit";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - Le droit \"".$nom_droit."\" a &eacute;t&eacute mis &agrave; jour.<br />";
			}
			elseif($action=="insert"){ //ajout d'un nouveau droit
				$sql = "INSERT INTO utilisateurs.bib_droits
						VALUES('$id_droit','$nom_droit','$desc_droit')";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - Le droit \"".$nom_droit."\" a &eacute;t&eacute; ajout&eacute;.<br />";
			}
			elseif($action=="delete"){ //ajout d'un nouveau droit
				$sql = "DELETE FROM utilisateurs.bib_droits
						WHERE id_droit = $id_droit";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - Le droit \"".$nom_droit."\" a &eacute;t&eacute; supprim&eacute;.<br />";
			}
			pg_close($dbconn);
		}
		else{$txt="connection impossible &agrave; la base ".$db_fun_name.".<br />";}
		$msg=$msg.$txt;
	}
}
header('Content-type: text/html');
echo "{success: true, msg:'".$msg."'}";
?>

