import pytest

from src.base.browser_manager import BrowserManager
from src.components.popups import Popups
from src.pages_object.home_page import HomePage
from src.pages_object.login_page import LoginPage
from src.pages_object.trade_page import TradePage


@pytest.fixture(scope="package")
def pages():
    page = BrowserManager.get_page()
    loginPage = LoginPage(page)
    homePage = HomePage(page)
    tradePage = TradePage(page)
    popupsPage = Popups(page)

    class PageContainer:
        login_page = loginPage
        home_page = homePage
        trade_page = tradePage
        popups = popupsPage

    return PageContainer
