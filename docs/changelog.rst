=========
CHANGELOG
=========

2.0.3 (2019-02-27)
------------------

**Nouveautés**

* Mise en place de logs rotatifs pour éviter de surcharger le serveur

**Corrections**

* Correction de l'enregistrement du formulaire des groupes qui passait automatiquement le champs ``t_roles.active`` à ``false`` (#71)
* Redirection de l'utilisateur si il n'a pas les droits suffisants pour accéder à une page
* Correction du script de migration 1.3.0to1.3.1.sql
* Correction de conflit d'authentification entre les différentes applications utilisant le sous-module d'authentification (MAJ du sous module en 1.3.2)

**Note de version** 

* Afin que les logs de l'application (supervisor et gunicorn) soient tous écrits au même endroit, éditez le fichier ``usershub-service.conf`` (``sudo nano /etc/supervisor/conf.d/usershub-service.conf``. A la ligne ``stdout_logfile``, remplacer la ligne existante par : ``stdout_logfile = /home/<MON_USER>/usershub/var/log/errors_uhv2.log`` (en remplaçant ``<MON_USER>`` par votre utilisateur linux).
* Vous pouvez également mettre en place un système de logs rotatifs (système permettant d'archiver les fichiers de log afin qu'ils ne surchargent pas le serveur) - conseillé si votre serveur a une capacité disque limitée. Créer le fichier suivant ``sudo nano /etc/logrotate.d/uhv2`` puis copiez les lignes suivantes dans le fichier nouvellement créé (en remplaçant ``<MON_USER>`` par votre utilisateur linux)

  ::

    /home/<MON_USER>/usershub/var/log/*.log {
    daily
    rotate 8
    size 100M
    create
    compress
    }

  Exécutez ensuite la commande ``sudo logrotate -f /etc/logrotate.conf``

* Suivez la procédure standard de mise à jour de UsersHub : https://usershub.readthedocs.io/fr/latest/installation.html#mise-a-jour-de-l-application

2.0.2 (2019-01-18)
------------------

**Corrections**

* Correction de la documentation
* Correction des versions du sous-module d'authentification

**Notes de version**

* Vous pouvez passer directement de la version 1.3.3 à la version 2.0.2, mais en suivant les notes de version de la 2.0.0.
* Si vous mettez à jour depuis la version 2.0.0, suivez la procédure classique de mise à jour (https://usershub.readthedocs.io/fr/latest/installation.html#mise-a-jour-de-l-application)

2.0.1 (2019-01-18)
------------------

**Corrections**

* Corrections mineures de l'authentification et de la gestion des sessions
* Mise à jour des scripts de synchronisation du schéma ``utilisateurs`` entre BDD mère et BDD filles (``data/synchro_interbase_fille.sql``	et ``data/synchro_interbase_mere.sql``). A tester et finaliser.

**Notes de version**

* Vous pouvez passer directement de la version 1.3.3 à la version 2.0.1, mais en suivant les notes de version de la 2.0.0.
* Si vous mettez à jour depuis la version 2.0.0, suivez la procédure classique de mise à jour (https://usershub.readthedocs.io/fr/latest/installation.html#mise-a-jour-de-l-application)

2.0.0 (2019-01-15)
------------------

Refonte complète de l'application en Python / Flask / Bootstrap 4

**Nouveautés**

* Suppression de la notion de droits à 6 niveaux (trop restrictive)
* Intégration de la notion de profils personalisables pour chaque application
* Mise en place d'une API pour pouvoir interroger et implémenter UsersHub depuis des applications tiers (#47)
* Simplification globale du MCD pour déporter la complexité côté metier et se rapprocher d'une application UsersHub type CAS
* Suppression des tags trop génériques (#28)
* Suppression du CRUVED, réintegré dans GeoNature (28#issuecomment-440293296)
* Création de vues assurant la rétrocompatibilité avec d'autres applications utilisant le modèle de la version 1 de UsersHub
* Création de fiches d'information permettant de faire une synthèse rapide par utilisateur, groupes, organisme ou application
* Ménage et ajouts de champs dans les tables ``t_role`` (suppression de ``nom_organisme``), ``bib_organimses`` (ajout ``url_organisme`` et ``url_logo``) et ``t_applications`` (``code_application`` #54)
* Automatisation de l'installation et révision du script ``install_app.sh``
* Contrôle de la cohérence entre les champs ``pass`` et ``pass_plus``
* Possibilité de ne pas utiliser le champs ``pass`` (md5) si on ne l'utilise pas pour renforcer la sécurité du contenu
* Développement de pages d'information par utilisateur, groupe, organisme, liste et application

**Notes de version**

Pour mettre à jour UsersHub depuis la version 1, il s'agit d'une nouvelle installation et d'une migration des données vers le nouveau modèle de BDD.

* Pour migrer depuis la version 1.3.3, suivez la documentation spécifique de migration (https://usershub.readthedocs.io/fr/latest/migration-v1v2.html)
* Pas de migration disponible depuis la version 2.0.0-beta.1

1.3.3 (2018-10-17)
------------------

**Corrections**

* Suppression de ``cor_role_droit_application`` inutiles
* ``install_app.sh`` : Suppression de messages portant à confusion

1.3.2 (2018-09-20)
------------------

**Corrections**

* Installation BDD : Nettoyage des données insérées et remise à 1 des séquences par défaut
* Vérification que le mot de passe encrypté en md5 et sha soient cohérents (#34)

2.0.0-beta.1 (2018-06-29)
-------------------------

Refonte totale de l'application en Python, Flask, Jinja, Bootstrap, Jquery. Par @Laumond11u.

* Rapport de stage : http://geonature.fr/documents/2018-06-usershub-v2-rapport-stage-Gabin-Laumond.pdf
* Présentation de stage : http://geonature.fr/documents/2018-06-usershub-v2-soutenance-stage-Gabin-Laumond.pdf

.. image :: http://geonature.fr/img/uhv2-screenshot.png

**Nouveautés**

* Interface de gestion des tags et de leurs types
* Interface de gestion des CRUVED
* Fiche rôle permettant d'afficher le détail des groupes, tags et CRUVED d'un rôle (utilisateur ou groupe)
* Fiche organisme permettant d'afficher le détail des membres et tags d'un organisme
* Suppression de tables (``t_menus``, ``bib_droits``, ``cor_role_menu``) et création de vues avec le même nom pour garder la compatibilité des applications basées sur UsersHub v1
* Table ``cor_role_droit_application`` remplacée par ``cor_role_tag_application``
* Compléments des données minimales (tags, types de tags...)
* Modification de la vue ``v_useraction_forall_gn_modules`` qui retourne le CRUVED d'un utilisateur pour pouvoir aussi récupérer le CRUVED d'un groupe

**Note de version**

* Version beta à ne pas utiliser en production
* Installation : https://github.com/PnEcrins/UsersHub/issues/35
* Exécuter le script de mise à jour de la BDD ``data/update_1.3.1to2.sql`` (attention il ne migre pas encore les données UsersHub V1)
* Renseigner les fichiers ``settings.ini`` et ``config.py`` à partir des samples

1.3.1 (2018-05-17)
------------------

**Nouveautés**

* Préparation dans la BDD d'une future version 1.4.0 (dont les extensions sont utilisées dans le développement de GeoNature2) :
  
  - Intégration d'un mécanisme générique d'étiquettes (tags) permettant une gestion des droits par actions sur des objets. Ce mécanisme permet aussi d'affecter des étiquettes à des roles, des organismes ou des applications. Il permet également de gérer la notion de portée des actions sur différentes étendue de données (mes données seulement, celles de mon organisme, toutes les données)
  - Intégration d'une hiérarchie entre applications et organismes (``id_parent``).
  - Pour le moment, ces extensions du modèle ne concernent que la base de données et pas l'interface de l'application.
* Mise en paramètre du cost de l'algorythme de criptage bcrypt
* Configuration Apache dans un fichier ``usershub.conf`` comme TaxHub et GeoNature-atlas

**Corrections**

* Ajout du ``pass_plus`` dans toutes les vues
* Correction de l'installation (localisation du ``config.php``)
* Ajout d'une vue manquante et nécessaire au sous-module d'authentification
* Interdire la création d'utilisateur avec l'organisme 0 (= ALL = tous les organismes) ; Utilisé dans GeoNature2 pour définir des paramètres applicables à tous les organismes.

**Notes de version**

* Ajouter le paramètre ``$pass_cost`` dans le ``config/config.php`` et lui donner une valeur éventuellement différente. Plus la valeur est importante, plus le temps de calcul de hashage du mot de passe est important.
* Exécuter le script ``data/update1.3.0to1.3.1.sql``
* Reporter les modifications dans les bases filles.
* Facultatif : revoir la configuration apache qui est maintenant dans un fichier usershub.conf (voir la doc). Ne pas oublier de supprimer le lien symbolique dans ``/var/www/html``


1.3.0 (2017-12-11)
------------------

**Changements**

* Mise en paramètre du port PostgreSQL pour l'installation initiale
* Intégration d'UUID pour les organismes et les roles afin de permettre des consolidations de bases utilisateurs
* Intégration d'un mécanisme d'authentification plus solide à base de hachage du mot de pass sur la base de l'algorithme ``bscript``. L'ancien mécanisme encodé en md5 (champ ``pass``) reste utilisable. Attention ceci ne concerne que l'authentification à UsersHub. Pour utiliser le hash dans d'autres applications, il faudra modifier les applications concernées et utiliser le nouveau champ ``pass_plus`` à la place du champ ``pass``.
* Création d'un formulaire permettant aux utilisateurs de mettre à jour leur mot de passe et de générer le nouveau hachage du mot de passe (http://mondomaine.fr/usershub/majpass.php).

**Notes de version**

* Les modifications de la BDD (ajout champ ``pass_plus`` notamment) doivent concerner la BDD principale de UsersHub (BDD mère) mais aussi toutes les BDD filles inscrites dans le fichier ``dbconnexions.json``. Pour cela 2 scripts sont proposés : ``data/update_mère_1.2.1to1.3.0.sql`` et ``data/update_filles_1.2.1to1.3.0.sql``.
* Synchroniser les UUID vers les BDD filles. Le script SQL appliqué sur la BDD mère va générer des UUID pour chaque utilisateur et organisme. S'il était appliqué sur les BDD filles, les UUID générés seraient différents de ceux de la BDD mère. Il faut donc les générer une seule fois dans la BDD mère, puis les copier dans les BDD filles. Pour cela, après s'être authentifié dans UsersHub il suffit de lancer le script ``web/sync_uuid.php`` : http://mondomaine.fr/usershub/sync_uuid.php. ATTENTION, ce script utilise le fichier ``dbconnexions.json`` pour boucler sur les BDD filles, il ne fonctionnera que si vous avez préalablement mis à jour toutes les BDD filles inscrites dans ``dbconnexions.json``.
* Créer le fichier ``config/config.php`` à partir du fichier ``config/config.php.sample`` et choisissez le mécanisme d'authentification à UsersHub que vous souhaitez mettre en place, ainsi que la taille minimale des mots de passe du nouveau champs ``pass_plus``. Il est conseillé de conserver le mot de passe ``pass`` (encodé en md5) le temps de mettre à jour les mots de passe des utilisateurs de UsersHub.
* Générer le hash des mots de passe, au moins pour les utilisateurs de UsersHub. Il existe trois manières de le faire :

  - lors de l'authentification de l'utilisateur, le hash du mot de pass qu'il vient de saisir est généré dans le champ ``pass_plus``.
  - en resaisissant le passe des utilisateurs dans le formulaire ``utilisateur``.
  - lors de la création d'un nouvel utilisateur, le hash est également généré (ainsi que le md5).
  - il n'est pas possible de générer le hash du mot de passe des utilisateurs existant à partir du mot de pass enregistré dans le champ ``pass`` (encodé en md5). Pour cela, diffusez le formulaire ``majpass.php`` qui permet aux utilisateurs de mettre à jour leur mot de passe et de générer le hash (ainsi que de mettre à jour le md5) avec l'adresse : http://mondomaine.fr/usershub/majpass.php


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
