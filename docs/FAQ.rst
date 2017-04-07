FAQ
===

Comment utiliser UsersHub ?
---------------------------

- Commencer par créer des organismes
- Puis créer des utilisateurs
- Les ajouter à des groupes
- Eventuellement ajouter des groupes dans les différentes listes
- Donner des droits à des groupes dans chaque application

.. image :: docs/images/usershub-applications.jpg

Quelles sont les applications compatibles et leurs niveaux de droits ?
----------------------------------------------------------------------

**TaxHub** :

- 2 = Gestion des médias uniquement
- 3 = Idem 2 + Gestion des attributs de GeoNature-atlas
- 4 = Idem 3 + Possibilité d'ajouter des taxons dans bib_noms, de les mettre dans des listes et de renseigner tous leurs attributs (notamment ceux utilisés par GeoNature)
- 6 = Administrateurs

**GeoNature V1** : 

- 2 = Rédacteurs qui peuvent saisir dans tous les protocoles, modifier leurs propres données et exporter les données de leur organisme
- 6 = Administrateurs qui peuvent modifier toutes les données

**Geotrek** (https://github.com/GeotrekCE/Geotrek-admin) :

Nécessite d'activer l'authentification externe (https://geotrek.readthedocs.io/en/master/advanced-configuration.html#external-authent) et de créer une vue dans la BDD de UsersHub qui renvoie les informations à plat comme indiqué dans la documentation de Geotrek.

- 1 = Lecture et export dans tous les modules
- 2 = Rédacteur (création, modification, suppression) dans les modules Sentiers, Statuts, Aménagements, Signalétique, Interventions et Chantiers) + Lecture et export dans tous les modules
- 3 = Référent Sentiers pouvant en plus créer, modifier et supprimer dans le module Tronçons. Accès à l'AdminSite pour gérer les valeurs des listes déroulantes des modules de gestion.
- 4 = Référent Communication pouvant lire et exporter dans tous les modules. Création, modification et suppression dans les modules Itinéraires, POIs, Contenus et Evenements touristiques, Services. Accès à l'AdminSite pour gérer les valeurs des listes déroulantes des modules de gestion.
- 6 = Administrateurs pouvant créer, modifier et supprimer dans tous les modules. 

Les autorisations relatives à chaque niveau de droit sont modifiables, groupe par groupe et objet par objet dans l'AdminSite de Geotrek.

**Police** (https://github.com/PnEcrins/Police) : 

- 1 = Lecture uniquement
- 2 = Rédacteurs pouvant créer des interventions et modifier leurs interventions
- 3 = Référents pouvant modifier, supprimer ou exporter toutes les interventions et renseigner les informations sur les suites données aux interventions
- 6 = Administrateurs. Idem au niveau 3.

**PatBati** (https://github.com/PnEcrins/PatBati) :

- 1 = Lecture
- 6 = Création, modification, suppression
