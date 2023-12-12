import logging
import os

from datetime import datetime
from playwright.sync_api import Page, BrowserContext, Browser

from utils.endpoints import Endpoints
import utils.requester as req
from tests.ui.pages.BasePage import BasePage
from tests.ui.pages.CreateProjectPage import CreateProjectPage
from tests.ui.pages.CreateTasksPage import CreateTasksPage
from tests.ui.pages.SideBar import SideBar


date = datetime.now().strftime("%d_%h_%Y_%H-%m-%S")
report_folder = os.path.join(os.getcwd(), "reports", f"{date}")
if not os.path.exists(report_folder):
    os.makedirs(report_folder)
log_path = os.path.join(report_folder, "orb_tests.log")
logging.basicConfig(filename=log_path, format="[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s")
LOGGER = logging.getLogger(__name__)


class SessionHelper:
    def __init__(self, browser, context, env):
        self.base_url = None
        self.env = env
        self.browser: Browser = browser
        self.context: BrowserContext = context
        self.is_signed_in = {"role": None, "done": False, "csrf": None}
        self.current_file = os.path.dirname(os.path.realpath(__file__))
        self.report_path = report_folder
        self.get_url()
        self.last_request = {}
        self.clean_up = []

    def get_url(self):
        links = {
            "dev1": "https://dev1.orb.com/",
            "stgqa": "https://prod.orb.com/"
        }
        LOGGER.info(f"Resolved link is {links[self.env]}")
        self.base_url = links[self.env]


class Application:
    def __init__(self, session, page):
        self.project_input_data = None
        self.page: Page = page
        self.session: SessionHelper = session
        self.env = session.env
        self.base_url = session.base_url
        self.endpoints = Endpoints
        self.requester = req
        self.side_bar = SideBar(page, self.base_url)
        self.base_page = BasePage(page, self.base_url)
        self.create_project = CreateProjectPage(page, self.base_url)
        self.tasks_creation = CreateTasksPage(page, self.base_url)
        self.users = {
            "SupperAdmin": {
                "login": "orb.at.super.manager@gmail.com",
                "password": "Test%sfera%1"
            },
            "Freelancer": {
                "login": "orb.at.freelancer@gmail.com",
                "password": "Test%sfera%1"
            },
            "Translator": {
                "login": "orb.at.translator@gmail.com",
                "password": "Test%sfera%1"
            },
            "UserEng": {
                "login": "user.orb.english.user@gmail.com",
                "password": "TestTest_12!"
            },
            "UserTranslator": {
                "login": "user.orb.translator@gmail.com",
                "password": "TestTest_12!"
            },
            "VendorTranslator": {
                "login": "orb.at.v.translator@gmail.com",
                "password": "TestTest_12!"
            }
        }

    def set_user(self, role, csrf):
        self.session.is_signed_in["done"] = True
        self.session.is_signed_in["role"] = role
        self.session.is_signed_in["csrf"] = csrf

    def reset_user(self):
        self.session.is_signed_in["done"] = False
        self.session.is_signed_in["role"] = None
        self.session.is_signed_in["csrf"] = None

    def update_csrf(self):
        self.session.is_signed_in["csrf"] = self.base_page.get_csrf_token()
