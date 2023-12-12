import logging

from playwright.sync_api import TimeoutError

from tests.ui.pages.BasePage import BasePage
from tests.ui.pages.selectors.create_project import CreateProject
from utils.endpoints import Endpoints

LOGGER = logging.getLogger(__name__)


class CreateProjectPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)

    def direct_open_create_project_page(self):
        self.page.goto(self.base_url + Endpoints.project_creation.create_project, timeout=60000)
        self.page.wait_for_selector(CreateProject.page_title)
        self.page.wait_for_load_state()

    # General Project Information section
    def set_client(self, client):
        element = self.page.query_selector(CreateProject.client_input)
        element.select_option(client)
        self.page.wait_for_timeout(800)  # Wait for filter rule apply (owner, distributor, product field)

    def set_owner(self, owner):
        element = self.page.query_selector(CreateProject.owner_input)
        element.select_option(owner)
        self.page.wait_for_timeout(800)  # Wait for filter rule apply (owner, distributor, product field)

    def set_distributor(self, distributor):
        element = self.page.query_selector(CreateProject.distributor_input)
        element.select_option(distributor)
        self.page.wait_for_timeout(800)  # Wait for filter rule apply (owner, distributor, product field)

    def set_product(self, product):
        element = self.page.wait_for_selector(CreateProject.product_input)
        element.select_option(product)
        self.page.wait_for_timeout(800)  # Wait for filter rule apply (owner, distributor, product field)

    def set_project_delivery_facilities(self, value: list or str):
        element = self.page.query_selector(CreateProject.project_delivery_facilities_multichoice)
        element.evaluate("e => e.style.display = 'block'")
        element.select_option(value)
        element.evaluate("e => e.style.display = 'none'")

    def set_test_practice(self, checkbox: bool):
        element = self.page.query_selector(CreateProject.test_practice_checkbox)
        element.evaluate("e => e.style.left = 0")
        element.set_checked(checkbox)
        element.evaluate("e => e.style.left = '-9999px'")

    def set_management_team(self, value: list or str):
        element = self.page.query_selector(CreateProject.management_team_multichoice)
        element.evaluate("e => e.style.display = 'block'")
        element.select_option(value)
        element.evaluate("e => e.style.display = 'none'")

    def set_project_manager(self, value: list or str):
        element = self.page.query_selector(CreateProject.project_manager_multichoice)
        element.evaluate("e => e.style.display = 'block'")
        element.select_option(value)
        element.evaluate("e => e.style.display = 'none'")

    def set_project_client_coordinator(self, value: str):
        element = self.page.query_selector(CreateProject.project_client_coordinator_select)
        element.evaluate("e => e.style.display = 'block'")
        element.select_option(value)
        element.evaluate("e => e.style.display = 'none'")

    def set_tiers(self, value: list or str):
        element = self.page.query_selector(CreateProject.project_projectTiers_multichoice)
        element.evaluate("e => e.style.display = 'block'")
        element.select_option(value)
        element.evaluate("e => e.style.display = 'none'")

    # Title and Version Info section
    def set_project_atlas_content_owner(self, value: str):
        self.page.query_selector(CreateProject.project_atlas_content_owner_input).select_option(value)

    def set_title_name(self, value: str):
        self.page.query_selector(CreateProject.title_name_input_area).click()
        self.page.query_selector(CreateProject.title_name_search_field).fill(value)
        self.page.wait_for_selector(f"span >> text={value}").click()

    def set_version_name(self, value: str):
        self.page.query_selector(CreateProject.version_name_input_area).click()
        self.page.wait_for_selector(f"div.select2-result-label >> text='{value}'").click()

    # Video Asset Information section
    def set_video_location(self, env):

        self.page.query_selector(CreateProject.view_assets_btn).click(timeout=5000)
        self.page.query_selector(CreateProject.root_folder).click(timeout=5000)
        self.page.wait_for_timeout(500)
        self.page.on("dialog", lambda dialog: dialog.accept())
        if env == "dev1":
            self.page.wait_for_selector(CreateProject.dev1_date_folder).click(timeout=5000)
            self.page.wait_for_timeout(500)
            self.page.wait_for_selector(CreateProject.dev1_asset_folder).click(timeout=5000)
            self.page.wait_for_timeout(1000)
            self.page.wait_for_selector(CreateProject.dev1_asset_file).click(timeout=5000)
        elif env == "stgqa":
            self.page.wait_for_selector(CreateProject.stgqa_date_folder).click(timeout=5000)
            self.page.wait_for_timeout(500)
            self.page.wait_for_selector(CreateProject.stgqa_asset_folder).click(timeout=5000)
            self.page.wait_for_timeout(1000)
            self.page.wait_for_selector(CreateProject.stgqa_asset_file).click(timeout=5000)
        for _ in range(2):
            self.close_pop_up_if_exist()

    def set_delivery_format(self, value: str):
        self.page.query_selector(CreateProject.delivery_format_input).select_option(value)

    def create_project(self):
        self.page.query_selector(CreateProject.next_btn).click(timeout=5000)

    def accept_similar_project_creation(self):
        try:
            self.page.wait_for_selector(CreateProject.similar_project_warning_accept_btn, timeout=5000).click()
        except TimeoutError:
            LOGGER.info("Similar projects were not found")

    def decline_similar_project_creation(self):
        try:
            self.page.wait_for_selector(CreateProject.similar_project_warning_decline_btn, timeout=5000).click()
        except TimeoutError:
            LOGGER.info("Similar projects were not found")

    def close_pop_up_if_exist(self):
        try:
            self.page.wait_for_selector(CreateProject.close_dialog_window_btn, timeout=5000).click()
            LOGGER.info("Pop up window was closed")
        except TimeoutError:
            pass
