import functools
import re
import logging
from flask import flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError

log = logging.getLogger()


def handle_db_errors(
    redirect_endpoint, entity_name="l'élément", redirect_on_error=True
):
    """
    Décorateur Flask pour capturer les erreurs de base de données (IntegrityError)
    et les erreurs générales, avec messages adaptés selon la méthode HTTP utilisée.

    :param redirect_endpoint: Nom de l'endpoint Flask pour la redirection après erreur.
    :param entity_name: Nom de l'entité concernée (ex : "l'utilisateur").
    :param redirect_on_error: Si True (défaut), effectue une redirection avec flash. Sinon, relance l'exception.
    """

    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapped_view(*args, **kwargs):
            # Identifier l'action utilisateur en fonction de la méthode HTTP
            action_label = {
                "GET": "l'affichage",
                "POST": "la création",
                "PUT": "la mise à jour",
                "PATCH": "la mise à jour",
                "DELETE": "la suppression",
            }.get(request.method, "le traitement")

            try:
                return view_func(*args, **kwargs)
            except IntegrityError as e:
                error_message = str(e.orig)
                detail_match = re.search(
                    r"DETAIL:\s*(.*)", error_message, re.IGNORECASE
                )
                if detail_match:
                    detail_message = detail_match.group(1)
                    flash(
                        f"{entity_name.capitalize()} ne peut pas être modifié lors de {action_label} : {detail_message}",
                        "error",
                    )
                else:
                    flash(
                        f"Une erreur est survenue lors de {action_label} de {entity_name}.",
                        "error",
                    )

                log.error(
                    f"Erreur d'intégrité pendant {action_label} de {entity_name} : {error_message}",
                    exc_info=True,
                )

                if redirect_on_error:
                    return redirect(url_for(redirect_endpoint))
                raise
            except Exception as e:
                flash(
                    f"Une erreur est survenue lors de {action_label} de {entity_name}.",
                    "error",
                )
                log.error(
                    f"Erreur générale pendant {action_label} de {entity_name} : {e}",
                    exc_info=True,
                )

                if redirect_on_error:
                    return redirect(url_for(redirect_endpoint))
                raise

        return wrapped_view

    return decorator
