<?php 
include "verification.php";

$txt = 'Base mère : '.$base.'</br>';
$txt .= '<hr/>';

require("../config/connecter.php");
// construction de la liste des uuid des roles
$sql = "SELECT id_role, uuid_role FROM utilisateurs.t_roles WHERE uuid_role IS NOT NULL;";
$result_roles = pg_query($sql) or die ("Erreur requête01") ;
$array_roles = array();
while ($row = pg_fetch_row($result_roles)) {
    array_push($array_roles, array($row[0],$row[1]));
}
// construction de la liste des uuid des roles organismes
$sql = "SELECT id_organisme, uuid_organisme FROM utilisateurs.bib_organismes WHERE uuid_organisme IS NOT NULL;";
$result_organisme = pg_query($sql) or die ("Erreur requête02") ;
$array_organismes = array();
while ($row = pg_fetch_row($result_organisme)) {
    array_push($array_organismes, array($row[0],$row[1]));
}

pg_close($dbconn);
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
        //connexion sur chacune des bases autre que la base mère
        if($connect_dbname != $base){
            if ($connect_host<>"" AND $connect_dbname<>"" AND $connect_user<>"" AND $connect_pass<>"") {
                $dbconnect = pg_connect("host=$connect_host port=$connect_port dbname=$connect_dbname user=$connect_user password=$connect_pass"); 
                foreach ($array_roles as $role){
                    $sql = "UPDATE utilisateurs.t_roles SET uuid_role = '".$role[1]."' WHERE id_role = ".$role[0];
                    if(pg_query($sql)){$txt .= "Base ".$db_fun_name." --> ID_ROLE : ".$role[0]." avec UUID ".$role[1]."<br/>";} 
                    else{$txt .= "Base ".$db_fun_name." --> ID_ROLE : ".$role[0]." erreur de mise &agrave; jour.<br/>";}
                }
                foreach ($array_organismes as $org){
                    $sql = "UPDATE utilisateurs.bib_organismes SET uuid_organisme = '".$org[1]."' WHERE id_organisme = ".$org[0];
                    if(pg_query($sql)){$txt .= "Base ".$db_fun_name." --> ID_ORGANISME : ".$org[0]." avec UUID ".$org[1]."<br/>";} 
                    else{$txt .= "Base ".$db_fun_name." --> ID_ORGANISME : ".$org[0]." erreur de mise &agrave; jour.<br/>";}
                }
                $txt .= "<hr/>";
                pg_close($dbconnect);
            }
            else{$txt.="connection impossible &agrave; la base ".$db_fun_name.".<br />";}
        }
        else{$txt.='On ne modifie pas la base mère "'.$base.'".';}
    }
}// fin de bouclage sur les bases
echo $txt;
?>

