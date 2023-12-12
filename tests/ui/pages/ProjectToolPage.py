import logging

from tests.ui.pages.BasePage import BasePage
from tests.ui.pages.selectors.project_tool import ProjectTool

LOGGER = logging.getLogger(__name__)


class CreateTasksPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)

    def wait_page(self):
        self.page.wait_for_selector(ProjectTool.page_title, timeout=60000)
        self.page.wait_for_load_state()

