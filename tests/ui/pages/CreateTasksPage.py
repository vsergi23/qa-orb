import logging
import re

from tests.ui.pages.BasePage import BasePage
from tests.ui.pages.selectors.create_project import TasksCreation

LOGGER = logging.getLogger(__name__)


class CreateTasksPage(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)

    def wait_page(self):
        self.page.wait_for_selector(TasksCreation.page_title, timeout=60000)
        self.page.wait_for_load_state()

    def save_jobs(self):
        self.page.wait_for_selector(TasksCreation.save_jobs_btn).click()

    def read_project_number(self):
        project_id = re.search(r"projectId=(\d{6})", self.page.url).group(1)
        if project_id:
            return project_id
        else:
            LOGGER.info(f"Can't find a project number in link: {self.page.url}")
            raise Exception(f"Can't find a project number in link: {self.page.url}")
