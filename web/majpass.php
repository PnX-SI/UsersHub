<?php
error_reporting(E_ERROR | E_WARNING | E_PARSE);

if(PHP_VERSION_ID<50500){require("../lib/password.php");}
require("../config/config.php");
function testpass($pass)
{
	require("../config/config.php");
	if (strlen($pass) >= $minimal_pass_len){
		return true;
	}
	return false;
}

$erreur = '';
$txt = '';

if (isset ($_POST['button'])){
	if (($_POST['button'] == "CONNEXION")){
		//récupération des données du formulaire
		$login = stripslashes($_POST['flogin']);
		$oldpass = stripslashes($_POST['foldpass']);
		$newpass = stripslashes($_POST['fnewpass']);
		$newpassbis = stripslashes($_POST['fnewpassbis']);
		$passmd5old = md5($oldpass);

		//vérification de l'utiliateur et de l'ancien pass
		require("../config/connecter.php");
		$sql = "SELECT * FROM utilisateurs.t_roles u WHERE u.identifiant = '".$login."' AND u.pass = '".$passmd5old."'";
		$result = pg_query($sql) or die ("Erreur requête02") ;
		$verif = pg_numrows($result);
		$dat = pg_fetch_assoc($result);
		$id_role = $dat['id_role'];
		//vérification de l'authentification
		if ($verif == "1"){
			//vérification de la validité du nouveau mot de passe
			if (testpass($newpass)){
				//vérification de la concordance des deux mots de passe
				if (($newpass == $newpassbis)){
					$passmd5new = md5($newpass); //calcul du nouveau pass md5
					$passplus = password_hash($newpass,PASSWORD_BCRYPT,['cost' => 13]); //calcul du hash pour le nouveau pass
					//mise à jour dans la base mère
					$query = "UPDATE utilisateurs.t_roles SET pass = '".$passmd5new ."', pass_plus = '".$passplus ."' WHERE id_role = '".$id_role."'";
					$sql_update = pg_query($query) or die ("Erreur requête 01") ;
					pg_close($dbconn);
					//mise à jour dans les bases filles
					$connexionsfile = "../config/dbconnexions.json";
					$f = fopen ($connexionsfile, "r");
					$dbconnexions = fread ($f, filesize($connexionsfile));
					fclose ($f);
					$json = json_decode($dbconnexions,true);
					foreach ($json as $array) {
						foreach ($array as $database) {
							$db_fun_name = str_replace("'","\'",$database['dbfunname']);
							$connect_host = $database['host'];
							$connect_dbname = $database['dbname'];
							$connect_user = $database['user'];
							$connect_pass = $database['pass'];
							$connect_port = $database['port'];
							//connexion sur chacune des bases 
							if($connect_dbname != $base){
								if ($connect_host<>"" AND $connect_dbname<>"" AND $connect_user<>"" AND $connect_pass<>"") {
									$dbconnect = pg_connect("host=$connect_host port=$connect_port dbname=$connect_dbname user=$connect_user password=$connect_pass"); 
									$sql = "UPDATE utilisateurs.t_roles SET pass = '".$passmd5new ."', pass_plus = '".$passplus ."' WHERE id_role = '".$id_role."'";
									$result = pg_query($sql) or die ('Erreur requête 02') ;
									$txt .= $db_fun_name." - Mise &agrave; jour.<br />";
									pg_close($dbconnect);
								}
								else{$txt .= "Connection impossible &agrave; la base ".$db_fun_name.".<br />";}
							}
						}
					}// fin de bouclage sur les bases
				}
				else{$erreur='<img src="images/supprimer.gif" alt="" align="absmiddle">&nbsp;Non concordance : les deux mots de passe ne correspondent pas';}
			}
			else{$erreur='<img src="images/supprimer.gif" alt="" align="absmiddle">&nbsp;Le nouveau mot de passe doit comporter au moins '.$minimal_pass_len.' caractères.';}
		}
		else{$erreur='<img src="images/supprimer.gif" alt="" align="absmiddle">&nbsp;Erreur d\'authentification. Utilisateur ou ancien mot de passe non valide.';}
	}
}
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Mise à jour des mots de passe</title>
<style type="text/css">
<!--
body {
	background-color: #D7E3B5;
	font-family: Trebuchet MS;
	font-weight: normal;
	font-size: 10pt;
}
-->
</style>
</head>
<body>
<form name="formlogin" method="post" action="majpass.php">
  <p>&nbsp;</p>
  <table width="300" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0" valign="center" align="center">
<tr>
	<td colspan="2" align="center" bgcolor="#5f5f5b"><img src="images/main_logo.png" alt="Logo" border="1" style="border-color:#f0f0f0"></td>
</tr>
</table>
 <table width="300" border="0" cellspacing="2" cellpadding="10" bgcolor="#f0f0f0" align="center">
	<tr>
		<td colspan="2" bgcolor="d5d5c2" align="center">
			<span class="Style1"><b>MISE A JOUR DE MON MOT DE PASSE</b></span>
		</td>
	</tr>
	<? if ($erreur){ ?>
		<tr><td colspan="2" class="Style1"><?=$erreur;?></td></tr>
	<? } ?>

	<tr>
		<td valign="top">Utilisateur</td>
		<td><span id="vlogin"><input type="text" class="Style2" id="login" name="flogin" value="<?=$login;?>" size="25"></span>
		</td>
	</tr>
	<tr>
		<td valign="top">Ancien pass</td>
		<td><span><input type="password" class="Style2" id="oldpassword" name="foldpass" value="<?=$oldpass;?>" size="25"></span>
		</td>
	</tr>
	<tr>
		<td valign="top">Nouveau pass</td>
		<td><span><input type="password" class="Style2" id="newpassword" name="fnewpass" value="<?=$newpass;?>" size="25"></span>
		</td>
	</tr>
	<tr>
		<td valign="top">Vérification pass</td>
		<td><span><input type="password" class="Style2" id="checkpassword" name="fnewpassbis" value="<?=$newpassbis;?>" size="25"></span>
		</td>
	</tr>
	<tr>
		<td colspan="2" align="center"><input type="submit" name="button" id="button" value="CONNEXION">    </td>
	</tr>

	<? if ($txt){ ?>
		<tr><td colspan="2" bgcolor="#CCC" class="Style1"><?=$txt;?></td></tr>
	<? } ?>

	<tr>
		<td colspan="2" bgcolor="#A9A7A8" align="center"><span class="Style4">&copy; 2017 - Parc national des Ecrins </span></td>
	</tr>
</table>
</form>
</body>
</html>