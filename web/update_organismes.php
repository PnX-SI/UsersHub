<?php
include "verification.php";
$id_organisme =  $_GET['id_organisme'];
//correction des magic_quotes_gpc (protection des chaînes de caractères)
$nom_organisme = pg_escape_string($_GET['nom_organisme']);
if(isset($_GET['adresse_organisme'])){$adresse_organisme=pg_escape_string($_GET['adresse_organisme']);}else{$adresse_organisme=null;}
if(isset($_GET['cp_organisme'])){$cp_organisme=pg_escape_string($_GET['cp_organisme']);}else{$cp_organisme=null;}
if(isset($_GET['ville_organisme'])){$ville_organisme=pg_escape_string($_GET['ville_organisme']);}else{$ville_organisme=null;}
if(isset($_GET['tel_organisme'])){$tel_organisme=pg_escape_string($_GET['tel_organisme']);}else{$tel_organisme=null;}
if(isset($_GET['fax_organisme'])){$fax_organisme=pg_escape_string($_GET['fax_organisme']);}else{$fax_organisme=null;}
if(isset($_GET['email_organisme'])){$email_organisme=pg_escape_string($_GET['email_organisme']);}else{$email_organisme=null;}
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
			if($action=="update"){ //Update d'un organisme existant
				$sql = "Update utilisateurs.bib_organismes 
				set id_organisme = $id_organisme, 
				nom_organisme = '$nom_organisme',
				adresse_organisme = '$adresse_organisme',
				cp_organisme = '$cp_organisme',
				ville_organisme = '$ville_organisme',
				tel_organisme = '$tel_organisme',
				fax_organisme = '$fax_organisme',
				email_organisme = '$email_organisme'
				WHERE id_organisme = $id_organisme";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'organisme \"".$nom_organisme."\" a &eacute;t&eacute mis &agrave; jour.<br />";
			}
			elseif($action=="insert"){ //ajout d'un nouvel organisme
				$sql = "INSERT INTO utilisateurs.bib_organismes
						VALUES('$nom_organisme','$adresse_organisme','$cp_organisme','$ville_organisme','$tel_organisme','$fax_organisme','$email_organisme',$id_organisme)";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'organisme \"".$nom_organisme."\" a &eacute;t&eacute; ajout&eacute;.<br />";
			}
			elseif($action=="delete"){ //ajout d'un nouvel organisme
				$sql = "DELETE FROM utilisateurs.bib_organismes
						WHERE id_organisme = $id_organisme";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'organisme \"".$nom_organisme."\" a &eacute;t&eacute; supprim&eacute;.<br />";
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