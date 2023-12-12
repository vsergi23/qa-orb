import logging
import re

from pytest_bdd import then, when, parsers
from playwright.sync_api import expect
from utils.helper import Application


LOGGER = logging.getLogger(__name__)


@when(parsers.parse('I follow link <{link}>'))
def follow_http(app, link):
    app.session.last_request = {"status_code": app.page.goto(link).status}
    app.page.wait_for_load_state()


@then(parsers.parse("URL redirects to <{link}>"))
def verify_https(app, link):
    url = app.page.url
    LOGGER.info(f"Redirected Link: {url}")
    assert url == link, "Service did not redirect to secure connection"


@then(parsers.parse("response code is <{status_code}>"))
def response_is_ok(app: Application, status_code):
    actual_status_code = app.session.last_request.get("status_code")
    if actual_status_code:
        assert int(actual_status_code) == int(status_code), \
            f"Status code {actual_status_code} doesn't equal expected status code {status_code}"
    else:
        raise Exception("Status code can't be pulled from response")


@when(parsers.parse('I open "{page_name}" in section "{section}"'))
def open_menu_page(app: Application, page_name: str, section: str):
    app.side_bar.open(section, page_name)


@then(parsers.parse('"{page_name}" page in section "{section}" is successfully loaded'))
def verify_page(app: Application, page_name: str, section: str):
    selector = app.side_bar.get_verify_selector(section, page_name)
    endpoint = app.side_bar.get_endpoint(section, page_name)
    app.side_bar.wait_loading()
    LOGGER.info("URL " + app.page.url)
    LOGGER.info("Expected URL " + app.base_url + endpoint)
    actual_url = app.page.url

    # hack to remove get parameters from link
    if "?" in actual_url.split("/")[-1]:
        actual_url = "/".join(actual_url.split("/")[:-1]) + "/" + actual_url.split("/")[-1].split("?")[0]
    # except a random number verification in link
    if "rand=" in app.page.url:
        actual_url = re.sub(r"rand=\d{,3}", "rand=", actual_url)

    assert actual_url.endswith(endpoint), f"Element of menu linked to wrong path." \
                                            f"\nActual url: {app.page.url}" \
                                            f"\nExpected: {app.base_url + endpoint}"
    app.page.wait_for_selector(selector)
    expect(app.page.locator(selector)).to_be_visible()
