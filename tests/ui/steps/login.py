import logging

from playwright.sync_api import TimeoutError
from pytest_bdd import parsers, then, given, when

from tests.ui.pages.selectors.common import Header
from tests.ui.pages.selectors.login import LoginPage
from tests.ui.pages.selectors.table_dashboard import TableDashboard
from utils.helper import Application

LOGGER = logging.getLogger(__name__)


@when(parsers.parse('I login with role <{role}> with UI'))
def log_in_ui(app: Application, role):
    login = app.users[role]['login']
    password = app.users[role]['password']
    if app.session.is_signed_in.get("done"):
        app.requester.logout(app)
    app.session.last_request = {"status_code": app.page.goto(app.base_url).status}
    basic_login_steps(app.page, login, password)


@given(parsers.parse('signed-in user as "{role}"'))
def login_session(app: Application, role: str):
    login = app.users[role]['login']
    password = app.users[role]['password']

    if app.session.is_signed_in["done"] and app.session.is_signed_in["role"] == role:
        check_request = app.page.request.get(app.base_url + 'messageCenter/webservice/newMessageCheck')
        if check_request.status == 200:
            app.page.goto(app.base_url + "admin/jobs/dashboardNewest")
        else:
            app.page.goto(app.base_url)
            basic_login_steps(app.page, login, password)
    else:
        app.page.goto(app.base_url)
        basic_login_steps(app.page, login, password)

    app.set_user(role, app.base_page.get_csrf_token())


@then(parsers.parse("I log out using UI"))
def ui_log_out(app: Application):
    app.page.query_selector(Header.log_out_btn).click(timeout=5000)
    app.page.query_selector(Header.yes_confirm_log_out).click(timeout=2000)
    app.page.wait_for_selector(LoginPage.log_in_btn)
    app.reset_user()


@then(parsers.parse("I log out"))
def log_out(app):
    app.page.goto(app.base_url + "site/logout")
    app.page.wait_for_selector("#login-button")


def basic_login_steps(page, login, password):
    page.wait_for_load_state()
    page.wait_for_selector(LoginPage.log_in_btn)
    page.query_selector(LoginPage.log_in_btn).click()
    page.wait_for_selector(LoginPage.login_pop_up)
    page.query_selector(LoginPage.email_field).fill(login)
    page.query_selector(LoginPage.password_field).fill(password)
    page.query_selector(LoginPage.login_submit_btn).click()
    try:
        page.wait_for_selector(LoginPage.session_warning_pop_up, timeout=4000)
        page.query_selector(LoginPage.session_warning_btn).click()
        LOGGER.info("Session conflict was resolved")
    except TimeoutError:
        LOGGER.info("Session conflict was not found")
    page.wait_for_selector(LoginPage.agreement_pop_up)
    page.locator(LoginPage.agreement_accept_btn).click()
    page.wait_for_selector(TableDashboard.form_window)
    page.wait_for_load_state()
