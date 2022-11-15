======
Docker
======

Image Docker de UsersHub
========================

L’image Docker de UsersHub vous permet de lancer UsersHub et de le connecter à votre serveur PostgreSQL existant.
Si vous n’avez pas de serveur PostgreSQL, ou que vous ne souhaitez pas l’utiliser, utilisez plutôt `Docker Compose`_.

Prérequis
---------

* Avoir un serveur PostgreSQL fonctionnel, avec une base de données crées dédiée à UsersHub, et des identifiants associés.
* Installer `Docker Engine <https://docs.docker.com/engine/install/debian/>`_

Utilisation
-----------

* Récupérer l’image :

.. code-block:: bash

    docker pull ghcr.io/pnx-si/usershub:latest

* Créer un conteneur à partir de l’image UsersHub et le démarrer :

.. code-block:: bash

    docker run \
        -d \
        --name usershub \
        -e USERSHUB_SQLALCHEMY_DATABASE_URI="postgresql://username:password@localhost/dbname" \
        --network=host \
        ghcr.io/pnx-si/usershub:latest

* Vérifier que l’image est bien lancé en accédant aux logs :

.. code-block:: bash

    docker logs usershub -f

* Créer le schéma de base de données :

.. code-block:: bash

    docker exec -it usershub flask db exec 'create extension if not exists "uuid-ossp"'
    docker exec -it usershub flask db upgrade usershub@head
    docker exec -it usershub flask db upgrade usershub-samples@head  # utilisateur admin / admin


Vous pouvez à présent vous rendre sur `http://localhost:5001`_ et vous connecter avec le couple identifiant / mot de passe ``admin`` / ``admin``.

Autres opérations utiles :

* Stopper UsersHub : ``docker stop usershub``
* Démarrer UsersHub : ``docker start usershub``
* Redémarrer UsersHub : ``docker restart usershub``
* Supprimer le conteneur UsersHub : ``docker rm usershub``. Le conteneur doit préalablement avoir été stoppé, et il peut être re-créé avec la commande ``docker run``.

Configuration
-------------

* Créer un fichier ``config.py`` avec le contenu suivant :

.. code-block:: python

    from app.config import *

    SECRET_KEY = "my secret key"
    SQLALCHEMY_DATABASE_URI = "…"

* Supprimer le conteneur et le re-créer :

.. code-block:: bash

    docker stop usershub
    docker rm usershub
    docker run \
        -d \
        --name usershub \
        --mount type=bind,source=$(realpath config.py),target=/dist/config.py \
        -e USERSHUB_SETTINGS=/dist/config.py \
        --network="host" \
        ghcr.io/pnx-si/usershub:latest

* À chaque modification du fichier ``config.py``, redémarrer le conteneur :

.. code-block:: bash

    docker restart usershub

Mise à jour
-----------

* Récupérer la dernière version de l’image :

.. code-block::bash

    docker pull ghcr.io/pnx-si/usershub:latest

* Supprimer le conteneur :

.. code-block:: bash

    docker stop usershub
    docker rm usershub

* Le recréer avec la commande ``docker run`` (voir ci-dessus)

* Mettre à jour la base de données :

.. code-block:: bash

    docker exec --it usershub flask db autoupgrade


Docker Compose
==============

Docker Compose vous permet de lancer UsersHub et un serveur PostgreSQL dédié automatiquement.

Prérequis
---------

* `Installer Docker Compose <https://docs.docker.com/compose/install/linux/#install-using-the-repository>`_
* Récupérer et dé-archiver la dernière version du code source depuis `Github <https://github.com/PnX-SI/UsersHub/releases>_`.

Installation
------------

* Ce rendre dans le dossier UsersHub : ``cd UsersHub``
* Installer le schéma utilisateurs en base : ``docker compose run --rm usershub flask db upgrade usershub@head``
* Installer les données d’exemple (utilisateur admin) en base : ``docker compose run --rm usershub flask db upgrade usershub-samples@head``
* Lancer UsersHub : ``docker compose up -d``

Vous pouvez à présent vous rendre sur `<http://localhost:5001>`_ et vous connecter avec le couple login / mot de passe ``admin`` / ``admin``.

Autres opérations utiles :

* Accéder aux logs : ``docker compose logs usershub -f``
* Stopper les conteneurs : ``docker compose stop``
* Redémarrer UsersHub : ``docker compose restart usershub``
* Supprimer les conteneurs : ``docker compose down``

Configuration
-------------

* Créer un fichier ``config/local_config.py`` :

.. code-block:: python

    from app.config import *

    SECRET_KEY = "my secret key"

* Indiquer à UsersHub d’utiliser votre fichier de configuration en créant un fichier ``.env`` contenant :

.. code-block:: bash

    USERSHUB_SETTINGS=/dist/config/local_config.py

* Lancer les containers – ils seront re-créés – afin d’utiliser votre nouveau fichier de configuration :

.. code-block:: bash

    docker compose up -d

* Au prochaines modifications du fichier ``local_config.py``, vous pouvez simplement redémarrer UsersHub :

.. code-block:: bash

    docker compose restart usershub

Mise à jour
-----------

.. code-block:: bash

    docker compose pull
    docker compose up -d
    docker compose run --rm usershub flask db autoupgrade

Modification du code source
---------------------------

À chaque modification du code source, vous devez :

* Builder l’image : ``docker compose build``
* Relancer : ``docker compose up -d``
