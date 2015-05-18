<?php 
include "verification.php";
if (isset($_GET['id_application'])){$id_application =$_GET['id_application'];}
if (isset($_GET['nom_application'])){$nom_application =$_GET['nom_application'];}
if($_GET['valeurs']!= null){
	$ids = $_GET['valeurs'];
	$array_valeurs = explode("-",$ids);	
}
else{
	$msg= "Attention ! Aucun role s&eacute;lectionn&eacute; ! <br/>";
}
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
			if($id_application>0){
				//on supprime d'abord les valeurs du groupe déjà enregistré
				$sql = "delete from utilisateurs.cor_role_droit_application WHERE id_application=$id_application";
				$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon.'.$db_fun_name.'"}') ;
				//puis on recréé les nouveaux
				foreach ($array_valeurs as $mes_ids){
					$array_ids = explode(",",$mes_ids);
					$role=$array_ids[0];
					$id_droit=$array_ids[1];
					$sql = "insert into utilisateurs.cor_role_droit_application (id_application, id_role, id_droit)
					values( $id_application, $role, $id_droit)";
					$result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon.'.$db_fun_name.'"}') ;
				}
        //-- Execution des commandes sql complémentaires
        if ((isset($database['autresactions'])) && (isset($database['autresactions']['cor_droits']))) {
          $sql = str_replace('$id',$id_application , $database['autresactions']['cor_droits']);
          $result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon autres actions.'.$db_fun_name.' "  }') ;
          $txt_autre = '<span style="color:green;"> autre action  r&eacute;alis&eacute;e.</span><br />';
        }
        else {
          $txt_autre = '';
        }
				$txt = $db_fun_name." - Les droits de l\'".$nom_application." ont &eacute;t&eacute mis &agrave; jour.<br />".$txt_autre;
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

