<?php
include "verification.php";
$id_unite =  $_GET['id_unite'];
//correction des magic_quotes_gpc (protection des chaînes de caractères)
$nom_unite = pg_escape_string($_GET['nom_unite']);
if(isset($_GET['adresse_unite'])){$adresse_unite=pg_escape_string($_GET['adresse_unite']);}else{$adresse_unite=null;}
if(isset($_GET['cp_unite'])){$cp_unite=pg_escape_string($_GET['cp_unite']);}else{$cp_unite=null;}
if(isset($_GET['ville_unite'])){$ville_unite=pg_escape_string($_GET['ville_unite']);}else{$ville_unite=null;}
if(isset($_GET['tel_unite'])){$tel_unite=pg_escape_string($_GET['tel_unite']);}else{$tel_unite=null;}
if(isset($_GET['fax_unite'])){$fax_unite=pg_escape_string($_GET['fax_unite']);}else{$fax_unite=null;}
if(isset($_GET['email_unite'])){$email_unite=pg_escape_string($_GET['email_unite']);}else{$email_unite=null;}
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
			if($action=="update"){ //Update d'une unité existante
				$sql = "Update utilisateurs.bib_unites 
				set id_unite = $id_unite, 
				nom_unite = '$nom_unite',
				adresse_unite = '$adresse_unite',
				cp_unite = '$cp_unite',
				ville_unite = '$ville_unite',
				tel_unite = '$tel_unite',
				fax_unite = '$fax_unite',
				email_unite = '$email_unite'
				WHERE id_unite = $id_unite";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'unite \"".$nom_unite."\" a &eacute;t&eacute mis &agrave; jour.<br />";
			}
			elseif($action=="insert"){ //ajout d'une nouvelle unité
				$sql = "INSERT INTO utilisateurs.bib_unites
						VALUES('$nom_unite','$adresse_unite','$cp_unite','$ville_unite','$tel_unite','$fax_unite','$email_unite',$id_unite)";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'unite \"".$nom_unite."\" a &eacute;t&eacute; ajout&eacute;.<br />";
			}
			elseif($action=="delete"){ //ajout d'une nouvelle unité
				$sql = "DELETE FROM utilisateurs.bib_unites
						WHERE id_unite = $id_unite";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'unite \"".$nom_unite."\" a &eacute;t&eacute; supprim&eacute;.<br />";
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