from src.pages_object.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__account_id = self.page.get_by_test_id("login-user-id")
        self.__password = self.page.get_by_test_id("login-password")

    def login(self, user_id, password):
        self.__account_id.fill(str(user_id))
        self.__password.fill(str(password))
        self.page.keyboard.press(key="Enter")
