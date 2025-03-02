from playwright.sync_api import expect

from src.components.notifications import Notifications
from src.data.enums import SidebarOptions
from src.pages_object.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.notifications = Notifications(page)

    def __sidebar_options(self, options: SidebarOptions):
        return self.page.get_by_test_id(f"side-bar-option-{options.lower()}")

    # actions
    def __open_page(self, options: SidebarOptions):
        self.__sidebar_options(options).click()

    def open_trade_page(self):
        self.__open_page(SidebarOptions.TRADE.value)

    # verify
    def verify_login_succeeded(self):
        expect(self.__sidebar_options(SidebarOptions.TRADE.value)).to_be_visible(timeout=10000)
