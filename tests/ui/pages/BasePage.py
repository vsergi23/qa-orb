import logging

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

from tests.ui.pages.selectors.common import Base
from utils.endpoints import Endpoints

LOGGER = logging.getLogger(__name__)


class BasePage:
    def __init__(self, page, base_url):
        self.page: Page = page
        self.base_url = base_url

    def wait_loading(self):
        try:
            self.page.wait_for_selector(Base.waiter, timeout=10000)
        except PlaywrightTimeoutError as error:
            LOGGER.info("Waiter not found. Continue testing... Error: " + str(error))
        self.page.wait_for_load_state()

    def wait_render(self):
        self.page.wait_for_load_state()
        self.page.wait_for_timeout(1000)

    def direct_open_page(self, section: str, page: str):
        try:
            section_obj = getattr(Endpoints, section)
        except AttributeError as error:
            LOGGER.info(f"Section {section} in endpoints config doesn't exist.\nError: {error}")
            raise Exception(f"Section {section} in endpoints config doesn't exist.")
        try:
            endpoint = getattr(section_obj, page)
        except AttributeError as error:
            LOGGER.info(f"Section {section} in endpoints config doesn't exist.\nError: {error}")
            raise Exception(f"Section {section} in endpoints config doesn't exist.")

        self.page.goto(self.base_url + endpoint)
        self.page.wait_for_load_state()

    def get_csrf_token(self):
        return self.page.query_selector('meta[name="csrf-token"]').get_attribute("data-token")

