<?php
include "verification.php";
if (isset($_GET['id_groupe'])){$id_groupe =$_GET['id_groupe'];}
if($_GET['roles']!= null){
	$ids_utilisateur = $_GET['roles'];
	$nom_groupe = $_GET['nom_groupe'];
	$array_utilisateurs = explode(",",$ids_utilisateur);
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
                if($id_groupe>0){
                    //on supprime d'abord les utilisateurs du groupe déjà enregistré
                    $sql = "delete from utilisateurs.cor_roles WHERE id_role_groupe=$id_groupe";
                    print_r(pg_result_error(pg_query($sql)));
                    $result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon DELETE.'.$db_fun_name.' "  }') ;
                    //puis on recréé les nouveaux
                    foreach ($array_utilisateurs as $utilisateur){
                        $sql = "insert into utilisateurs.cor_roles (id_role_groupe, id_role_utilisateur)
                        values( $id_groupe, $utilisateur)";
                        $result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon INSERT. '.$db_fun_name.'" }') ;
                    }
                    //-- Execution des commandes sql complémentaires
                    if ((isset($database['autresactions'])) && (isset($database['autresactions']['cor_roles']))) {
                      $sql = str_replace('$id',$id_groupe , $database['autresactions']['cor_roles']);
                      $result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon autres actions.'.$db_fun_name.' "  }') ;
                      $txt_autre = '<span style="color:green;"> autre action  r&eacute;alis&eacute;e.</span><br />';
                    }
                    else {
                      $txt_autre = '';
                    }
                    $txt = $db_fun_name." - Le contenu du groupe \"".$nom_groupe."\" a &eacute;t&eacute; mis &agrave; jour.<br />".$txt_autre;
                }
                pg_close($dbconn);
            }
            else{$txt="connection impossible &agrave; l\'".$db_fun_name.".<br />";}
            $msg=$msg.$txt;
        }
    }
}
else{
	$msg= "Attention ! Aucun utilisateur s&eacute;lectionn&eacute; !";
}
header('Content-type: text/html');
echo "{success: true, msg:'".$msg."'}";
?>

