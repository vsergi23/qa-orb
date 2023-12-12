import logging
import os
from typing import Any

import allure
import pytest
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright, Error
from allure_commons.lifecycle import AllureLifecycle
from allure_commons.model2 import TestResult
from allure_commons import plugin_manager

from tests.ui.steps.login import login_session
from utils.helper import SessionHelper, Application

LOGGER = logging.getLogger(__name__)

# Import steps to use them anywhere
directory = "tests."
pytest_plugins = (
    directory + "ui.steps.login",
    directory + "ui.steps.common",
    directory + "ui.steps.project_workflows"
)


@pytest.fixture(scope="session")
def session(request):
    input_browser = request.config.option.browser
    env = request.config.option.env
    with sync_playwright() as page:
        browser = page[input_browser].launch()
        context = browser.new_context()
        session = SessionHelper(browser, context, env)
        try:
            yield session
        finally:
            clean(session)
            context.close()
            browser.close()
            LOGGER.info("Session is closed")
            LOGGER.info("Browser is closed")


@pytest.fixture(scope="function")
def app(session):
    page = session.context.new_page()
    application = Application(session, page)
    yield application
    page.close()


def pytest_addoption(parser: Any) -> None:
    group = parser.getgroup("qa-orb", "qa-localization-orb")
    group.addoption(
        "--browser",
        default="chromium",
        choices=["chromium", "firefox", "webkit"],
        help="Browser to launch tests",
    )
    group.addoption(
        "--env",
        default="dev1",
        choices=["dev1", "prod"],
        help="Select environment from list [dev1, prod] to run tests on different environments",
    )


def pytest_collection_modifyitems(config, items):
    if config.option.markexpr:
        config.option.markexpr = config.option.markexpr + " and " + config.option.env
    else:
        config.option.markexpr = config.option.env


def clean(session_obj):
    try:
        page = session_obj.context.new_page()
        app = Application(session_obj, page)
        if not session_obj.is_signed_in.get("done"):
            login_session(app, "SupperAdmin")
        if session_obj.clean_up:
            for clean_obj in session_obj.clean_up:
                obj_type = clean_obj.get("type")
                if obj_type == "project":
                    if clean_obj["tasks"]:
                        for task in clean_obj["tasks"]:
                            pass  # remove tasks
                    app.requester.post_remove_project(app, clean_obj["id"])
                elif obj_type == "other type":
                    pass
                else:
                    raise Exception("Unrecognized type of object in clean_up array")
    except Exception as e:
        LOGGER.error(f"Clean up wasn't finished.\nData {session_obj.clean_up}\nError: {e}")


def pytest_bdd_step_error(request, step, exception):
    LOGGER.warning(f"Step Failed {step}")
    app: Application = request.getfixturevalue("app")
    if not os.path.exists(app.session.report_path + "/screenshots"):
        os.makedirs(app.session.report_path + "/screenshots")
    file_name = str(step).replace(' ', '_').replace('"', "")
    full_path = app.session.report_path + f"/screenshots/{file_name}.png"
    screen = app.page.screenshot(path=full_path, full_page=True)
    allure.attach(screen, name="Screenshot", attachment_type=AttachmentType.PNG)


# this is custom decision while allure-pytest module has bag with json saving
def custom_write_test_case(self, uuid=None):
    test_result = self._pop_item(uuid=uuid, item_type=TestResult)
    if test_result:
        if test_result.parameters:
            adj_parameters = []
            for param in test_result.parameters:
                if param.name != '_pytest_bdd_example':
                    # do not include parameters with "_pytest_bdd_example"
                    adj_parameters.append(param)
            test_result.parameters = adj_parameters

        plugin_manager.hook.report_result(result=test_result)


AllureLifecycle.write_test_case = custom_write_test_case
