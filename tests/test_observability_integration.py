import json
import logging
import os
import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from sqlalchemy import select
import sqlalchemy as sa

from app.app import create_app
from app.env import db
from app.models import TRoles, Bib_Organismes, CorRoles, CorRoleListe
from pypnusershub.db.models import User
from pypnusershub.db.tools import user_to_token


REPO_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_ENV = "USERSHUB_TEST_SETTINGS"
LOGIN_ENV = "USERSHUB_TEST_LOGIN"
PASSWORD_ENV = "USERSHUB_TEST_PASSWORD"


class ListHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)

    def messages(self):
        return [self.format(record) for record in self.records]


def resolve_settings_path():
    configured = os.environ.get(SETTINGS_ENV)
    candidates = []
    if configured:
        candidates.append(Path(configured))
    candidates.append(REPO_ROOT / "config" / "config.py")

    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise unittest.SkipTest(
        "No UsersHub settings file found. Set USERSHUB_TEST_SETTINGS to a valid config path."
    )


class UsersHubObservabilityIntegrationTests(unittest.TestCase):
    @staticmethod
    def _has_organism_additional_data_column():
        columns = sa.inspect(db.engine).get_columns(
            "bib_organismes", schema="utilisateurs"
        )
        return any(column["name"] == "additional_data" for column in columns)

    @staticmethod
    def _find_first_scalar_value(value):
        if isinstance(value, dict):
            for item in value.values():
                candidate = UsersHubObservabilityIntegrationTests._find_first_scalar_value(item)
                if candidate not in (None, "", [], {}):
                    return candidate
            return None
        if isinstance(value, (list, tuple)):
            for item in value:
                candidate = UsersHubObservabilityIntegrationTests._find_first_scalar_value(item)
                if candidate not in (None, "", [], {}):
                    return candidate
            return None
        return value

    @classmethod
    def setUpClass(cls):
        settings_path = resolve_settings_path()
        os.environ["USERSHUB_SETTINGS"] = str(settings_path)
        cls.app = create_app()
        cls.app.testing = True
        cls.app.config.update(
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            ENABLE_REQUEST_LOGGING=True,
            ENABLE_SLOW_REQUEST_LOGGING=True,
            ENABLE_REQUEST_ERROR_LOGGING=True,
            ENABLE_SLOW_SQL_LOGGING=True,
            SLOW_REQUEST_THRESHOLDS_MS=(25, 100, 500),
            SLOW_SQL_THRESHOLD_MS=200,
        )
        cls.admin_login = os.environ.get(LOGIN_ENV, "admin")
        cls.admin_password = os.environ.get(PASSWORD_ENV)

        with cls.app.app_context():
            admin_user = db.session.execute(
                select(User).where(User.identifiant == cls.admin_login)
            ).scalar_one_or_none()
            if admin_user is None:
                raise unittest.SkipTest(
                    "Unable to find the configured test admin user in the local database."
                )
            cls.admin_user_id = admin_user.id_role
            user_with_additional_fields = (
                db.session.query(TRoles.id_role, TRoles.champs_addi)
                .filter(TRoles.champs_addi.isnot(None))
                .filter(TRoles.champs_addi != {})
                .first()
            )
            organism_with_additional_fields = None
            if cls._has_organism_additional_data_column():
                organism_with_additional_fields = db.session.execute(
                    sa.text(
                        """
                        SELECT id_organisme, additional_data
                        FROM utilisateurs.bib_organismes
                        WHERE additional_data IS NOT NULL
                          AND additional_data != '{}'::jsonb
                        LIMIT 1
                        """
                    )
                ).first()
            cls.user_with_additional_fields_id = (
                user_with_additional_fields[0] if user_with_additional_fields else None
            )
            cls.user_with_additional_fields_value = (
                cls._find_first_scalar_value(user_with_additional_fields[1])
                if user_with_additional_fields
                else None
            )
            cls.organism_with_additional_fields_id = (
                organism_with_additional_fields[0] if organism_with_additional_fields else None
            )
            cls.organism_with_additional_fields_value = (
                cls._find_first_scalar_value(organism_with_additional_fields[1])
                if organism_with_additional_fields
                else None
            )

    def setUp(self):
        self._handlers = []
        self.client = self.app.test_client()
        self.app.config["SLOW_SQL_THRESHOLD_MS"] = 200

    def tearDown(self):
        for logger, handler, previous_level, previous_propagate in self._handlers:
            logger.removeHandler(handler)
            logger.setLevel(previous_level)
            logger.propagate = previous_propagate
        self._handlers = []
        self.client.environ_base.pop("HTTP_AUTHORIZATION", None)

    def _capture_logger(self, logger_name, level=logging.INFO):
        logger = logging.getLogger(logger_name)
        handler = ListHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        previous_level = logger.level
        previous_propagate = logger.propagate
        logger.setLevel(level)
        logger.propagate = False
        logger.addHandler(handler)
        self._handlers.append((logger, handler, previous_level, previous_propagate))
        return handler

    @staticmethod
    def _first_scalar(query):
        row = query.first()
        return row[0] if row is not None else None

    def _login_with_token(self):
        with self.app.app_context():
            admin_user = db.session.get(User, self.admin_user_id)
            self.client.environ_base["HTTP_AUTHORIZATION"] = (
                "Bearer " + user_to_token(admin_user).decode()
            )

    def test_login_with_password(self):
        if not self.admin_password:
            raise unittest.SkipTest(
                "Set USERSHUB_TEST_PASSWORD to run the authenticated login test."
            )

        response = self.client.post(
            "/pypn/auth/login",
            json={"login": self.admin_login, "password": self.admin_password},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("user", payload)
        self.assertEqual(payload["user"]["identifiant"], self.admin_login)
        self.assertIn("token", payload)
        self.assertIn("expires", payload)
        self.assertIn("X-Request-ID", response.headers)

    def test_protected_route_redirects_to_login_without_session(self):
        response = self.client.get("/users/list", follow_redirects=False)

        self.assertEqual(response.status_code, 302)
        redirect_url = urlsplit(response.headers["Location"])
        self.assertTrue(redirect_url.path.endswith("/login"))
        self.assertEqual(parse_qs(redirect_url.query).get("next"), ["/users/list"])
        self.assertIn("X-Request-ID", response.headers)

    def test_get_current_user_contract_stays_compatible_for_geonature_clients(self):
        self._login_with_token()

        response = self.client.get("/pypn/auth/get_current_user")

        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Request-ID", response.headers)
        payload = response.get_json()
        self.assertIn("user", payload)
        self.assertIn("token", payload)
        self.assertIn("expires", payload)
        self.assertEqual(payload["user"]["identifiant"], self.admin_login)

    def test_api_register_test_connexion_contract_stays_compatible_for_geonature_clients(self):
        self._login_with_token()

        response = self.client.get("/api_register/test_connexion")

        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Request-ID", response.headers)
        self.assertEqual(response.get_json(), {"msg": "connexion ok"})

    def test_users_list_logs_metrics_and_matches_db_count(self):
        request_log = self._capture_logger("usershub.observability")
        slow_request_log = self._capture_logger("usershub.request.slow", level=logging.WARNING)
        slow_sql_log = self._capture_logger("usershub.sql.slow", level=logging.WARNING)
        self._login_with_token()
        self.app.config["SLOW_SQL_THRESHOLD_MS"] = 0

        with self.app.app_context():
            expected_count = (
                db.session.query(TRoles).filter(TRoles.groupe.is_(False)).count()
            )

        html_response = self.client.get("/users/list")
        html = html_response.get_data(as_text=True)
        response = self.client.get(
            "/users/list?draw=1&start=0&length=25&order[0][column]=1&order[0][dir]=asc"
        )
        payload = response.get_json()

        self.assertEqual(html_response.status_code, 200)
        self.assertIn('data-server-side="true"', html)
        self.assertIn("data-ajax-url=\"/users/list\"", html)

        self.assertEqual(response.status_code, 200)
        self.assertIn("X-Request-ID", response.headers)
        self.assertEqual(payload["recordsTotal"], expected_count)
        self.assertEqual(payload["recordsFiltered"], expected_count)
        self.assertEqual(len(payload["data"]), 25)
        self.assertIn("action_info", payload["data"][0])

        request_messages = request_log.messages()
        slow_request_messages = slow_request_log.messages()
        slow_sql_messages = slow_sql_log.messages()

        self.assertTrue(
            any("request_completed" in message and "/users/list" in message for message in request_messages)
        )
        self.assertTrue(any("rendered_object_count" in message for message in request_messages))
        self.assertTrue(any("users_list_fetch_duration_ms" in message for message in request_messages))
        self.assertTrue(any("users_list_prepare_duration_ms" in message for message in request_messages))
        self.assertTrue(any("users_list_total_count" in message for message in request_messages))
        self.assertTrue(any("users_list_filtered_count" in message for message in request_messages))
        self.assertTrue(
            any("slow_request" in message and "/users/list" in message for message in slow_request_messages)
        )
        self.assertTrue(any("slow_sql" in message for message in slow_sql_messages))

    def test_users_list_server_side_search_filters_results(self):
        self._login_with_token()

        response = self.client.get(
            "/users/list?draw=2&start=0&length=10&search[value]=admin"
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["draw"], 2)
        self.assertLessEqual(payload["recordsFiltered"], payload["recordsTotal"])
        self.assertLessEqual(len(payload["data"]), 10)
        self.assertGreater(payload["recordsFiltered"], 0)

    def test_users_list_server_side_status_filter_matches_db_count(self):
        self._login_with_token()

        with self.app.app_context():
            expected_active_count = (
                db.session.query(TRoles)
                .filter(TRoles.groupe.is_(False))
                .filter(TRoles.active.is_(True))
                .count()
            )

        response = self.client.get(
            "/users/list?draw=3&start=0&length=25&status_filter=true"
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["draw"], 3)
        self.assertEqual(payload["recordsFiltered"], expected_active_count)
        self.assertLessEqual(len(payload["data"]), 25)
        for row in payload["data"]:
            self.assertEqual(row["active"], "True")

    def test_users_list_server_side_inactive_filter_includes_false_and_null(self):
        self._login_with_token()

        with self.app.app_context():
            expected_inactive_count = (
                db.session.query(TRoles)
                .filter(TRoles.groupe.is_(False))
                .filter(sa.or_(TRoles.active.is_(False), TRoles.active.is_(None)))
                .count()
            )

        response = self.client.get(
            "/users/list?draw=4&start=0&length=25&status_filter=false"
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["draw"], 4)
        self.assertEqual(payload["recordsFiltered"], expected_inactive_count)
        self.assertLessEqual(len(payload["data"]), 25)
        for row in payload["data"]:
            self.assertEqual(row["active"], "False")

    def test_organism_autocomplete_api_returns_suggestions(self):
        self._login_with_token()

        response = self.client.get("/api/organisms/autocomplete?q=bre")

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIsInstance(payload, list)
        self.assertGreater(len(payload), 0)
        self.assertIn("id_organisme", payload[0])
        self.assertIn("nom_organisme", payload[0])
        self.assertIn("label", payload[0])

    def test_user_update_form_uses_autocomplete_and_group_checkboxes(self):
        self._login_with_token()

        response = self.client.get(f"/user/update/{self.admin_user_id}")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("organism-autocomplete", html)
        self.assertIn("/api/organisms/autocomplete", html)
        self.assertIn("group-choice-", html)

    def test_user_info_displays_additional_fields_generically(self):
        if not self.user_with_additional_fields_id or self.user_with_additional_fields_value in (None, ""):
            raise unittest.SkipTest("No user with additional fields found in the local database.")

        self._login_with_token()
        response = self.client.get(f"/user/info/{self.user_with_additional_fields_id}")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Champs additionnels", html)
        self.assertIn(str(self.user_with_additional_fields_value), html)

    def test_organisms_list_server_side_matches_db_count(self):
        request_log = self._capture_logger("usershub.observability")
        slow_request_log = self._capture_logger("usershub.request.slow", level=logging.WARNING)
        self._login_with_token()

        with self.app.app_context():
            expected_count = db.session.query(Bib_Organismes).count()

        html_response = self.client.get("/organisms/list")
        html = html_response.get_data(as_text=True)
        response = self.client.get(
            "/organisms/list?draw=1&start=0&length=25&order[0][column]=1&order[0][dir]=asc"
        )
        payload = response.get_json()

        self.assertEqual(html_response.status_code, 200)
        self.assertIn('data-server-side="true"', html)
        self.assertIn("data-ajax-url=\"/organisms/list\"", html)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload["recordsTotal"], expected_count)
        self.assertEqual(payload["recordsFiltered"], expected_count)
        self.assertEqual(len(payload["data"]), 25)
        self.assertIn("action_info", payload["data"][0])

        request_messages = request_log.messages()
        slow_request_messages = slow_request_log.messages()
        self.assertTrue(
            any("request_completed" in message and "/organisms/list" in message for message in request_messages)
        )
        self.assertTrue(any("organisms_list_page" in message for message in request_messages))
        self.assertTrue(any("list_total_count" in message for message in request_messages))
        self.assertTrue(any("list_filtered_count" in message for message in request_messages))
        self.assertTrue(
            any("slow_request" in message and "/organisms/list" in message for message in slow_request_messages)
        )

    def test_organisms_list_server_side_search_filters_results(self):
        self._login_with_token()

        with self.app.app_context():
            sample_organism = (
                db.session.query(Bib_Organismes.nom_organisme)
                .filter(Bib_Organismes.nom_organisme.isnot(None))
                .order_by(Bib_Organismes.nom_organisme.asc())
                .first()
            )
            self.assertIsNotNone(sample_organism)
            search_value = sample_organism[0][:8]

        response = self.client.get(
            f"/organisms/list?draw=2&start=0&length=10&search[value]={search_value}"
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["draw"], 2)
        self.assertLessEqual(payload["recordsFiltered"], payload["recordsTotal"])
        self.assertLessEqual(len(payload["data"]), 10)
        self.assertGreater(payload["recordsFiltered"], 0)

    def test_group_members_page_uses_server_side_pagination(self):
        self._login_with_token()

        with self.app.app_context():
            total_without_active_filter = (
                db.session.query(sa.func.count(TRoles.id_role))
                .filter(TRoles.id_role != 2)
                .filter(
                    ~TRoles.id_role.in_(
                        db.session.query(CorRoles.id_role_utilisateur).filter(
                            CorRoles.id_role_groupe == 2
                        )
                    )
                )
                .filter(
                    ~TRoles.id_role.in_(
                        db.session.query(CorRoles.id_role_groupe).filter(
                            CorRoles.id_role_utilisateur == 2
                        )
                    )
                )
                .scalar()
            )
            total_with_active_filter = (
                db.session.query(sa.func.count(TRoles.id_role))
                .filter(TRoles.id_role != 2)
                .filter(TRoles.active.is_(True))
                .filter(
                    ~TRoles.id_role.in_(
                        db.session.query(CorRoles.id_role_utilisateur).filter(
                            CorRoles.id_role_groupe == 2
                        )
                    )
                )
                .filter(
                    ~TRoles.id_role.in_(
                        db.session.query(CorRoles.id_role_groupe).filter(
                            CorRoles.id_role_utilisateur == 2
                        )
                    )
                )
                .scalar()
            )

        html_response = self.client.get("/group/members/2")
        html = html_response.get_data(as_text=True)
        response = self.client.get(
            "/group/members/2?panel=available&draw=1&start=0&length=25&order[0][column]=2&order[0][dir]=asc"
        )
        payload = response.get_json()

        self.assertEqual(html_response.status_code, 200)
        self.assertIn('data-membership-mode="true"', html)
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(payload["data"]), 25)
        self.assertIn("full_name", payload["data"][0])
        self.assertEqual(payload["recordsTotal"], total_without_active_filter)
        self.assertGreaterEqual(total_without_active_filter, total_with_active_filter)

    def test_group_members_selected_panel_handles_pending_add_and_del_consistently(self):
        self._login_with_token()

        with self.app.app_context():
            selected_id = self._first_scalar(
                db.session.query(CorRoles.id_role_utilisateur)
                .filter(CorRoles.id_role_groupe == 2)
                .order_by(CorRoles.id_role_utilisateur.asc())
            )
            candidate_add_id = self._first_scalar(
                db.session.query(TRoles.id_role)
                .filter(TRoles.id_role != 2)
                .filter(
                    ~TRoles.id_role.in_(
                        db.session.query(CorRoles.id_role_utilisateur).filter(
                            CorRoles.id_role_groupe == 2
                        )
                    )
                )
                .filter(
                    ~TRoles.id_role.in_(
                        db.session.query(CorRoles.id_role_groupe).filter(
                            CorRoles.id_role_utilisateur == 2
                        )
                    )
                )
                .order_by(TRoles.id_role.asc())
            )
            base_selected_count = (
                db.session.query(sa.func.count(CorRoles.id_role_utilisateur))
                .filter(CorRoles.id_role_groupe == 2)
                .scalar()
            )

        self.assertIsNotNone(selected_id)
        self.assertIsNotNone(candidate_add_id)

        response = self.client.get(
            "/group/members/2",
            query_string={
                "panel": "selected",
                "draw": 1,
                "start": 0,
                "length": -1,
                "pending_add": json.dumps([candidate_add_id]),
                "pending_del": json.dumps([selected_id]),
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        returned_ids = {row["id_role"] for row in payload["data"]}
        self.assertEqual(payload["recordsTotal"], base_selected_count)
        self.assertIn(candidate_add_id, returned_ids)
        self.assertNotIn(selected_id, returned_ids)

    def test_list_members_page_uses_server_side_pagination(self):
        self._login_with_token()

        with self.app.app_context():
            total_without_active_filter = (
                db.session.query(sa.func.count(TRoles.id_role))
                .filter(
                    ~db.session.query(CorRoleListe)
                    .filter(CorRoleListe.id_liste == 1)
                    .filter(CorRoleListe.id_role == TRoles.id_role)
                    .exists()
                )
                .scalar()
            )
            total_with_active_filter = (
                db.session.query(sa.func.count(TRoles.id_role))
                .filter(TRoles.active.is_(True))
                .filter(
                    ~db.session.query(CorRoleListe)
                    .filter(CorRoleListe.id_liste == 1)
                    .filter(CorRoleListe.id_role == TRoles.id_role)
                    .exists()
                )
                .scalar()
            )

        html_response = self.client.get("/list/members/1")
        html = html_response.get_data(as_text=True)
        response = self.client.get(
            "/list/members/1?panel=available&draw=1&start=0&length=25&order[0][column]=2&order[0][dir]=asc"
        )
        payload = response.get_json()

        self.assertEqual(html_response.status_code, 200)
        self.assertIn('data-membership-mode="true"', html)
        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(payload["data"]), 25)
        self.assertIn("full_name", payload["data"][0])
        self.assertEqual(payload["recordsTotal"], total_without_active_filter)
        self.assertGreaterEqual(total_without_active_filter, total_with_active_filter)

    def test_list_members_selected_panel_handles_pending_add_and_del_consistently(self):
        self._login_with_token()

        with self.app.app_context():
            selected_id = self._first_scalar(
                db.session.query(CorRoleListe.id_role)
                .filter(CorRoleListe.id_liste == 1)
                .order_by(CorRoleListe.id_role.asc())
            )
            candidate_add_id = self._first_scalar(
                db.session.query(TRoles.id_role)
                .filter(
                    ~db.session.query(CorRoleListe)
                    .filter(CorRoleListe.id_liste == 1)
                    .filter(CorRoleListe.id_role == TRoles.id_role)
                    .exists()
                )
                .order_by(TRoles.id_role.asc())
            )
            base_selected_count = (
                db.session.query(sa.func.count(CorRoleListe.id_role))
                .filter(CorRoleListe.id_liste == 1)
                .scalar()
            )

        self.assertIsNotNone(selected_id)
        self.assertIsNotNone(candidate_add_id)

        response = self.client.get(
            "/list/members/1",
            query_string={
                "panel": "selected",
                "draw": 1,
                "start": 0,
                "length": -1,
                "pending_add": json.dumps([candidate_add_id]),
                "pending_del": json.dumps([selected_id]),
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        returned_ids = {row["id_role"] for row in payload["data"]}
        self.assertEqual(payload["recordsTotal"], base_selected_count)
        self.assertIn(candidate_add_id, returned_ids)
        self.assertNotIn(selected_id, returned_ids)

    def test_user_update_groups_are_sorted_alphabetically(self):
        self._login_with_token()

        response = self.client.get(f"/user/update/{self.admin_user_id}")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        labels = re.findall(
            r'<label class="custom-control-label" for="group-choice-\d+">([^<]+)</label>',
            html,
        )
        self.assertGreater(len(labels), 1)
        self.assertEqual(labels, sorted(labels, key=lambda value: value.casefold()))

    def test_organism_info_displays_additional_fields_generically(self):
        if not self.organism_with_additional_fields_id or self.organism_with_additional_fields_value in (None, ""):
            raise unittest.SkipTest("No organism with additional fields found in the local database.")

        self._login_with_token()
        response = self.client.get(f"/organism/info/{self.organism_with_additional_fields_id}")
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Champs additionnels", html)
        self.assertIn(str(self.organism_with_additional_fields_value), html)

    def test_invalid_delete_returns_friendly_html_error_and_logs_request_context(self):
        error_log = self._capture_logger("app.utils.errors", level=logging.ERROR)
        self._login_with_token()

        response = self.client.get("/users/delete/999999999", follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Erreur base de donnees lors de la suppression.", html)
        self.assertIn("Request ID:", html)

        messages = error_log.messages()
        self.assertTrue(any("sqlalchemy_error" in message for message in messages))
        self.assertTrue(any("/users/delete/999999999" in message for message in messages))
        self.assertTrue(any("\"request_id\"" in message for message in messages))

    def test_invalid_delete_json_response_stays_minimal_and_exposes_request_id_in_header(self):
        self._login_with_token()

        response = self.client.get(
            "/users/delete/999999999",
            headers={"Accept": "application/json"},
        )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.mimetype, "application/json")
        self.assertIn("X-Request-ID", response.headers)

        payload = response.get_json()
        self.assertEqual(set(payload.keys()), {"message"})
        self.assertIn("Erreur base de donnees lors de la suppression.", payload["message"])


if __name__ == "__main__":
    unittest.main()
