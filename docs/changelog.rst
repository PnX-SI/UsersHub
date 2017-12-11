=========
CHANGELOG
=========

1.3.0 (2017-12-11)
------------------

**Changements**

* Intégration d'UUID pour les organismes et les roles afin de permettre des consolidations de bases utilisateurs
* Intégration d'un mécanisme d'authentification plus solide à base de haschage du mot de pass sur la base de l'algorythme ``bscript``. L'ancien mécanisme ``md5`` reste utilisable.
Attention ceci ne concerne que l'authentification à UsersHub. Pour utiliser le hash dans d'autres applications, il faudra modifier les applications concernées et utiliser le champ ``pass_plus`` à la place du champ ``md5``.
* Création d'un formulaire permettant aux utilisateurs de mettre à jour leur mot de passe et de générer le nouveau hachage du mot de passe.

**Notes de version**

* Les modification de la base doivent concerner la base principale de UsuersHub (base mère) mais aussi toutes les bases filles inscrites dans le fichier ``dbconnexions.json``.
Pour cela 2 scripts sont proposés.
    * ``data/update_mère_1.2.1to1.3.0.sql`` et ``data/update_filles_1.2.1to1.3.0.sql``.
* synchroniser les UUID vers les bases filles. Le script sql appliqué sur la base mère va générer des UUID pour chaque utilisateur et organisme. 
S'il était appliqué sur les bases filles, les UUID générés seraient différents de ceux de la base mère. 
Il faut donc les générer une seule fois dans la base mère, puis les copier dans les bases filles. Pour cela, après s'être authentifié dans UsersHub il suffit de lancer le script ``web/sync_uuid.php`` : http://mondomaine.fr/usershub/sync_uuid.php
ATTENTION, ce script utilise ``dbconnexions.json`` pour boucler sur les bases filles, il ne fonctionnera que si vous avez préalablement mise à jour toutes les bases filles inscrites dans ``dbconnexions.json``.
* Créer le fichier ``config/config.php`` à partir du fichier ``config/config.php.sample`` et choisissez le mécanisme d'authentification à UsersHub que vous souhaitez mettre en place, ainsi que la taille minimale des mots de passe.
Il est conseillé de conserver le ``md5`` le temps de mettre à jour les mots de passe des utilisateurs de UsersHub.
* Générer le hash des mots de passe, au moins pour les utilisateurs de UsersHub. Il existe trois manières de le faire :
    * lors de l'authentification de l'utilisateur, le hash du mot de pass qu'il vient de saisir est généré dans le champ ``pass_plus``.
    * en resaisissant le passe des utilisateurs dans le formulaire ``utilisateur``.
    * lors de la création d'un nouvel utilisateur, le hash est également généré (ainsi que le md5).
    * il n'est pas possible de générer le hach du mot de passe des utilisateurs existant à partir du mot de pass enregistré dans le champ ``pass``. 
    Pour cela, diffusez le formulaire ``majpass.php`` qui permet aux utilisateurs de mettre à jour leur mot de passe et de générer le hash (ainsi que le md5) avec l'adresse : http://mondomaine.fr/usershub/majpass.php


1.2.2 (2017-07-06)
------------------

**Changements**

* Correction du script SQL (remplacement de SELECT par PERFORM)
* Mise à jour du fichier ``settings.ini.sample`` pour prendre en compte le port
* Suppression de la référence au host databases (retour à localhost)

**Notes de version**

* Les modifications réalisée concerne une première installation, vous n'avez aucune action particulière à réaliser.


1.2.1 (2017-04-11)
------------------

**Changements**

* Gestion plus fine des erreurs dans le script SQL de création du schéma ``utilisateurs``, afin de pouvoir éxecuter le script sur une BDD existante
* Gestion des notices PHP
* Suppression d'une table inutile (``utilisateurs.bib_observateurs``)
* Correction de l'URL du logo du PNE
* Mise à jour du fichier ``web/js/settings.js.sample``
* Documentation - Ajout d'une FAQ et mise en forme

**Notes de version**

* Si vous mettez à jour l'application depuis la version 1.2.0, éxécutez le script ``data/update1.2.0to1.2.1.sql`` qui supprime la table inutile ``bib_observateurs``.

1.2.0 (2016-11-16)
------------------

**Changements**

* Compatibilité avec TaxHub accrue
* Bugfix
* Distinction groupe/utilisateurs dans les listes d'utilisateurs.
* Dépersonnalisation de la page de login et du bandeau.
* Désactivation de l'autoremplissage par défaut du mail de l'utilisateur. Reste possible mais optionnel.
* Tri par ordre alphabétiques des listes déroulantes.

1.1.2 (2016-11-02)
------------------

**Corrections**

* Prise en compte de TaxHub en tant qu'application à part entière avec ses utilisateurs et leurs droits.

1.1.1 (2016-10-26)
------------------

Corrections mineures

1.1.0 (2016-08-31)
------------------

**Changements**

* Ajout du port PostgreSQL (``port``) dans les paramètres de configuration (by Claire Lagaye PnVanoise)

A ajouter dans ``config/connecter.php`` et ``config/dbconnexions.json``.

Voir https://github.com/PnEcrins/UsersHub/blob/master/config/connecter.php.sample#L7 et https://github.com/PnEcrins/UsersHub/blob/master/config/dbconnexions.json.sample#L10

 
1.0.0 (2015-10-13)
------------------

* Première version stabilisée de l'application avec script d'installation automatique.


0.1.0 (2015-01-28)
------------------

* Mise en ligne du projet et de la documentation
