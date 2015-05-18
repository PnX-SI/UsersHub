UsersHub
=========

Application web de gestion centralisée des utilisateurs.

UsersHub est une application web permettant de regrouper l'ensemble des utilisateurs d'applications web afin de gérer de manière différenciée et centralisée les droits d'accès à ces applications ainsi que le contenu des listes déroulantes d'observateurs. 

Elle permet de gérer de manière centralisée **des utilisateurs** et de les placer dans **des groupes** ; de créer **différents niveaux de droits** et de les affecter aux utilisateurs et/ou aux groupes d'utilisateurs pour chacune de vos **applications**. Elle permet également de gérer **des organismes**, **des unités** et **des listes déroulantes** regroupant des utilisateurs ou des groupes d'utilisateurs.

Compatible avec GeoNature (https://github.com/PnEcrins/GeoNature) et Geotrek (https://github.com/makinacorpus/Geotrek).

Présentation
-----------

Principe général : UsersHub permet de gérer et de synchroniser le contenu d'un ou plusieurs schéma "utilisateurs" d'une ou plusieurs bases PostgreSQL. A condition que le modèle mais aussi que toutes les données de ces bases soient identiques, UsersHub permet de maintenir le contenu du schéma "utilisateurs" de ces bases strictement identique.

Dans un système d'information, les applications web 'métier' nécessitent généralement une identification par login/pass. 
Les applications disposent donc d'un dispositif de gestion des utilisateurs et de leur droits.
L'utilisateur n'a pas forcement les mêmes droits d'une application à l'autre et l'administrateur doit maintenir une liste d'utilisateurs dans chacune des applications. Ces applications ont le plus souvent chacune une base de données dédiée.
A condition d'organiser la gestion de ces utilisateurs de manière identique dans toutes les bases des applications web, UsersHub permet de centraliser cette gestion et de réaliser les modification dans toutes les bases en une seule opération.

UsersHub dispose de sa propre base de données mais utilise un fichier des settings permettant de déclarer les paramètres de connexion aux différentes bases.
Lorsqu'une modification est réaliser dans la base, elle est reproduite dans toutes les bases déclarées dans ce fichier de settings.
Si un utilisateur arrivent dans votre structure, si un mot de passe doit être changé, vous ne le faite qu'une seule fois.

Une fois enregistré, un utilisateur peut être placé dans un groupe et ses droits d'accès à telle ou telle application web sont hérités des droits du groupe.
Mais vous pouvez aussi affecter des droits spécifiques à un utilisateurs pour telle application  ou telle autre.
Si certains des utilisateurs ou groupe d'utilisateurs doivent figurer dans une liste déroulante de l'application (par exemple une liste d'observateurs ou de représentants), UsersHub permet de créer ces listes et d'en gérer le contenu. 
Il ne vous reste alors plus qu'à utiliser cette liste dans votre application.

.. image :: docs/images/capture-application.jpg

Installation
-----------

Consulter la documentation :  `<http://usershub.rtfd.org>`_

Ou dans docs/installation.rst

License
-------

* OpenSource - BSD
* Copyright (c) 2015 - Parc National des Écrins


.. image:: http://pnecrins.github.io/GeoNature/img/logo-pne.jpg
    :target: http://www.ecrins-parcnational.fr
