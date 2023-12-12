from tests.ui.pages.BasePage import BasePage
from tests.ui.pages.selectors.side_bar_config import router


class SideBar(BasePage):
    def __init__(self, page, base_url):
        super().__init__(page, base_url)

    def open(self, section_item, menu_item):
        section = self._get_section(section_item)
        menu_page = self._get_menu_item(section, menu_item)

        if menu_page:
            self.wait_render()
            if section and not self.page.is_visible(menu_page.element):
                if menu_page.parents:
                    if not self.page.is_visible(menu_page.parents[0]):
                        self.page.query_selector(section["this"]).click()
                else:
                    self.page.query_selector(section["this"]).click()
            if menu_page.parents:
                for el in menu_page.parents:
                    self.page.wait_for_load_state()
                    self.page.click(el)
            self.page.wait_for_selector(menu_page.element).click()
        else:
            raise Exception(f"Can't found menu item '{menu_item}' inside section '{section_item}' in side bar config")

    def get_verify_selector(self, section_item, menu_item):
        section = self._get_section(section_item)
        item = self._get_menu_item(section, menu_item)
        return item.verifying_selector

    def get_endpoint(self, section_item, menu_item):
        section = self._get_section(section_item)
        item = self._get_menu_item(section, menu_item)
        return item.endpoint

    @staticmethod
    def _get_section(section_item):
        section = router.get(section_item)
        if section:
            return section
        else:
            raise Exception(f"Can't found section '{section_item}' in side bar config")

    @staticmethod
    def _get_menu_item(section, menu_item):
        item = section.get(menu_item)
        if item:
            return item
        else:
            raise Exception(f"Can't found menu item '{menu_item}' in side bar config")
