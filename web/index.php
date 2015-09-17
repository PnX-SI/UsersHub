<?php
if ($_POST['button'] == "CONNEXION"){
	$login = $_POST['flogin'];
	$password = md5($_POST['fpassword']);
	require("../config/connecter.php");
	$query = "SELECT * FROM utilisateurs.t_roles u WHERE u.identifiant = '".$login."' AND u.pass = '".$password."'";
	$sql = pg_query($query) or die ("Erreur requête01") ;
	$verif = pg_numrows($sql);
	$dat = pg_fetch_assoc($sql);
		if ($verif == "1")
		{
            session_start();
			if (isset($_POST['flogin'])){
			$_SESSION['xlogin'] = $login;
			$_SESSION['xauthor'] = $dat['id_role'];
			$query = ("UPDATE utilisateurs.t_roles SET session_appli = '".session_id()."' WHERE id_role = '".$dat['id_role']."'");
			$sql_update = pg_query($query) or die ("Erreur requête") ;
			pg_close($dbconn);
			header("Location: accueil.php");
			}
		}
		
		else{
		$erreur='<img src="images/supprimer.gif" alt="" align="absmiddle">&nbsp;Login ou mot de passe incorrect';
		}
}
else{
	session_start();
	$_SESSION = array();
	if (isset($_COOKIE[session_name()])) {
	    setcookie(session_name(), '', time()-42000, '/');
	}
	session_destroy();
}
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Utilisateurs - Identification</title>
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
<form name="formlogin" method="post" action="index.php">
  <p>&nbsp;</p>
  <table width="300" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0" valign="center" align="center">
<tr>
	<td colspan="2" align="center" bgcolor="#740160"><img src="images/main_logo.png" alt="Parc national des Ecrins" border="1" style="border-color:#f0f0f0"></td>
</tr>
</table>
 <table width="300" border="0" cellspacing="2" cellpadding="10" bgcolor="#f0f0f0" align="center">
	<tr>
		<td colspan="2" bgcolor="#FCFDAF" align="center">
			<span class="Style1"><b>IDENTIFICATION</b></span>
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
    <td valign="top">Mot de passe</td>
    <td><span id="vpassword"><input type="password" class="Style2" id="password" name="fpassword" value="<?=$password;?>" size="25"></span>
	</td>
  </tr>
  <tr>
    <td colspan="2" align="center"><input type="submit" name="button" id="button" value="CONNEXION">    </td>
  </tr>
  <tr>
  	<td colspan="2" bgcolor="#A9A7A8" align="center"><span class="Style4">&copy; 2010 - Parc national des Ecrins </span></td>
  </tr>
</table>
</form>
</body>
</html>