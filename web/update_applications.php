<?php 
include "verification.php";
$id_application =  $_GET['id_application'];
//correction des magic_quotes_gpc (protection des chaînes de caractères)
$nom_application = pg_escape_string($_GET['nom_application']);
$desc_application = pg_escape_string($_GET['desc_application']);
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
			if($action=="update"){ //Update d'une application existante
				$sql = "Update utilisateurs.t_applications 
				set id_application = '$id_application', 
				nom_application = '$nom_application',
				desc_application = '$desc_application'
				WHERE id_application = $id_application";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'application ".$nom_application." a &eacute;t&eacute mis &agrave; jour.<br />";
			}
			elseif($action=="insert"){ //ajout d'une nouvelle application
				$sql = "INSERT INTO utilisateurs.t_applications
						VALUES('$id_application','$nom_application','$desc_application')";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'application ".$nom_application." a &eacute;t&eacute; ajout&eacute;.<br />";
			}
			elseif($action=="delete"){ //suppression d'une nouvelle application
				$sql = "DELETE FROM utilisateurs.t_applications
						WHERE id_application = $id_application";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - L\'application ".$nom_application." a &eacute;t&eacute; supprim&eacute;.<br />";
			}
			pg_close($dbconn);
		}
        else{$txt="connection impossible &agrave; la base ".$db_fun_name.".<br />";}
		$msg=$msg.$txt;
    }
}// fin de bouclage sur les bases

//retour json à l'application utilisateur
header('Content-type: text/html');
echo "{success: true, msg:'".$msg."'}";
?>

