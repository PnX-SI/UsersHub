<?php 
include "verification.php";

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
        $connect_port = $database['port'];
        //connexion sur chacune des bases 
		if ($connect_host<>"" OR $connect_dbname<>"" OR $connect_user<>"" OR $connect_pass<>"") {
			$dbconn = pg_connect("host=$connect_host port=$connect_port dbname=$connect_dbname user=$connect_user password=$connect_pass"); 
			$sql = "UPDATE utilisateurs.t_roles SET pass_plus = '".$passplus."' WHERE id_role = ".$dat['id_role'];
			$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
			$txt = $db_fun_name." - Le pass_plus a &eacute;t&eacute mis &agrave; jour.<br />";
			pg_close($dbconn);
		}
        else{$txt="connection impossible &agrave; la base ".$db_fun_name.".<br />";}
		$msg=$msg.$txt;
    }
}// fin de bouclage sur les bases
?>

