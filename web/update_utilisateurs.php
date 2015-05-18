<?php 
include "verification.php";
//récupération des variables passées par l'application
$id_role = $_GET['id_role'];
$nom_role =pg_escape_string($_GET['nom_role']);
if(isset($_GET['prenom_role'])){$prenom_role = pg_escape_string($_GET['prenom_role']);}else{$prenom_role= null;}
$role = $nom_role." ".$prenom_role;
if(isset($_GET['identifiant'])){$identifiant=$_GET['identifiant'];}else{$identifiant= null;}
if(isset($_GET['email'])){$email=$_GET['email'];}else{$email= null;}
if(isset($_GET['id_organisme'])){$id_organisme=$_GET['id_organisme'];}else{$id_organisme= null;}
if(isset($_GET['id_unite'])){$id_unite=$_GET['id_unite'];}else{$id_unite= null;}
if(isset($_GET['pass']) AND $_GET['pass']<>''){$pass=md5($_GET['pass']);}else{$pass= null;}
if(isset($_GET['supprpass'])){$supprpass='true';}else{$supprpass= 'false';}
if(isset($_GET['pn'])){$pn='true';}else{$pn= 'false';}
if(isset($_GET['remarques'])){
    $remarques=str_replace( array( CHR(10), CHR(13), "\n", "\r" ), array( ' - ',' - ',' - ',' - '), $_GET['remarques'] );
}else{
    $remarques= null;
}
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
            if($action=="insert"){ //ajout 
              if ($id_role == '' ){
                $sql = "INSERT INTO utilisateurs.t_roles (groupe,nom_role,prenom_role,identifiant,remarques,email,id_organisme,id_unite,pn, pass)
                        VALUES('false','$nom_role','$prenom_role','$identifiant','$remarques','$email',$id_organisme,$id_unite,'$pn','$pass') RETURNING id_role;";
                $result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon. '.$db_fun_name.' '.$sql.' "}') ;
                while ($row = pg_fetch_row($result)) {
                  $id_role =  $row[0];
                }
              }
              else {
                $sql = "INSERT INTO utilisateurs.t_roles (groupe,id_role, nom_role,prenom_role,identifiant,remarques,email,id_organisme,id_unite,pn, pass)
                        VALUES('false',$id_role, '$nom_role','$prenom_role','$identifiant','$remarques','$email',$id_organisme,$id_unite,'$pn','$pass');";
                pg_query($sql) or die ('{success: false, msg:"ben ! pas bon. '.$db_fun_name.' '.$sql.' "}') ;
              }
              $txt = $db_fun_name." - le role \"".$role."\" a &eacute;t&eacute; ajout&eacute;.<br />";
            }
            //Sinon, c'est un update ou delete donc on vérifie que le role existe dans la bd
            if($action=="update" OR $action=="delete"){
                $sql = "SELECT id_role FROM utilisateurs.t_roles WHERE id_role = $id_role";
                $res = pg_query($sql);
                $nb = pg_numrows($res);
                // si le role existe
                if ($nb>0){ 
                    if($action=="update"){ //modification
                        $sql = "Update utilisateurs.t_roles 
                        set nom_role = '$nom_role',
                        prenom_role = '$prenom_role',
                        identifiant = '$identifiant',
                        remarques = '$remarques',
                        email = '$email',
                        id_organisme = $id_organisme,
                        id_unite = $id_unite,
                        pn = '$pn'";
                        if($pass<>null||$pass<>''){$sql= $sql.",pass = '$pass'";}
                        $sql = $sql."WHERE id_role = $id_role";
                        if(pg_query($sql)){$txt = $db_fun_name." - le role \"".$role."\" a &eacute;t&eacute mis &agrave; jour.<br />";}
                        else{$txt = $db_fun_name.'<span style="color:red;"> - Erreur de mise &agrave; jour.</span><br />';}
                        if($supprpass=='true'){
                            $sql = "Update utilisateurs.t_roles set pass = null, identifiant = null WHERE id_role = $id_role";
                            if(pg_query($sql)){$txt = $txt." Mot de passe et identifiant supprim&eacute;s.<br />";}
                            else{$txt = $txt.'<span style="color:red;"> Mot de passe et identifiant non supprim&eacute;s.</span><br />';}
                        }
                    }
                    elseif($action=="delete"){ //suppression
                        $sql = "DELETE FROM utilisateurs.t_roles
                                WHERE id_role = $id_role";
                        if(pg_query($sql)){$txt = $db_fun_name." - le role \"".$role."\" a &eacute;t&eacute; supprim&eacute;.<br />";}
                        else{$txt = $db_fun_name.'<span style="color:red;"> - Erreur : role \''.$role.'\' non supprim&eacute;.</span><br />';}
                    }   
                }
                //si le role n'existe pas
                else{$txt = $db_fun_name.'<span style="color:red;"> - Erreur :  le role '.$id_role. ' n\\\'existe pas dans cette base.</span><br />';}   
            }
            //-- Execution des commandes sql complémentaires
            if ((isset($database['autresactions'])) && (isset($database['autresactions']['role_'.$action]))) {
              $sql = str_replace('$id',$id_role , $database['autresactions']['role_'.$action]);
              $result = pg_query($sql) or die ('{success: false, msg:"ben ! pas bon autres actions. '.$action.' '.$db_fun_name.' '.$sql.'" }') ;
              $txt .= '<span style="color:green;"> autre action '.$action.' r&eacute;alis&eacute;e.</span><br />';
            }
            pg_close($dbconn);//fermeture de la connexion pour pouvoir en ouvrir une autre dans la boucle
        }
		else{$txt="connection impossible &agrave; l\'".$db_fun_name.".<br />";}
		$msg=$msg.$txt;//On complète le message à afficher dans l'appli utilisateur avant de boucler
	}
}
header('Content-type: text/html');
echo "{success: true, msg:'".$msg."', id_role:".$id_role."}";
?>

