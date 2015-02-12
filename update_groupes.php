<?php 
include "verification.php";
$id_groupe =  $_GET['id_groupe'];
//correction des magic_quotes_gpc (protection des chaînes de caractères)
$nom_groupe =pg_escape_string($_GET['nom_groupe']);
$desc_groupe =pg_escape_string($_GET['desc_groupe']);
$action = $_GET['action'];
//-----------création des connections pour mise à jour sur les différentes bases du fichier dbconnexions.json------------
$fp = fopen ("config/dbconnexions.json", "r");
$contenu_du_fichier = fread ($fp, filesize('config/dbconnexions.json'));
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
			//exécution de la mise à jour dans toutes les bases 
			if($action=="update"){ //Update d'un groupe existant
				$sql = "Update utilisateurs.t_roles 
				set nom_role = '$nom_groupe',
				desc_role = '$desc_groupe'
				WHERE id_role = $id_groupe";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - Le groupe \"".$nom_groupe."\" a &eacute;t&eacute mis &agrave; jour.<br />";
        //-- Execution des commandes sql complémentaires
        if ((isset($database['autresactions'])) && (isset($database['autresactions']['groupe_update']))) {
          $sql = str_replace('$id',$id_groupe , $database['autresactions']['groupe_update']);
          $result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon autres actions. groupe_update'.$db_fun_name.' "  }') ;
        }
			}
			elseif($action=="insert"){ //ajout d'un nouveau groupe
				$sql = "INSERT INTO utilisateurs.t_roles (groupe,nom_role,desc_role)
						VALUES('true','$nom_groupe','$desc_groupe')";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - Le groupe \"".$nom_groupe."\" a &eacute;t&eacute; ajout&eacute;.<br />";
			}
			elseif($action=="delete"){ //ajout d'un nouveau groupe
				$sql = "DELETE FROM utilisateurs.t_roles
						WHERE id_role = $id_groupe";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon."}') ;
				$txt = $db_fun_name." - Le groupe \"".$nom_groupe."\" a &eacute;t&eacute; supprim&eacute;.<br />";
         //-- Execution des commandes sql complémentaires
        if ((isset($database['autresactions'])) && (isset($database['autresactions']['groupe_delete']))) {
          $sql = str_replace('$id',$id_groupe , $database['autresactions']['groupe_delete']);
          $result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon autres actions. groupe_delete'.$db_fun_name.' "  }') ;
        }
			}
			pg_close($dbconn);
		}
		else{$txt="connection impossible &agrave; l\'".$db_fun_name.".<br />";}
		$msg=$msg.$txt;
	}
}
header('Content-type: text/html');
echo "{success: true, msg:'".$msg."'}";
?>

