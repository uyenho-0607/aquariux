from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

from src.utils.logging_utils import logger


class BrowserManager:
    __browser: Browser = None
    __page: Page = None
    __plw: Playwright = None
    __context: BrowserContext = None

    @classmethod
    def init_browser(cls, browser_type="chrome", headless=False):
        plw = sync_playwright().start()

        match browser_type:
            case "chrome":
                cls.__browser = plw.chromium.launch(channel="chrome", headless=headless, slow_mo=500)
            case "firefox":
                cls.__browser = plw.firefox.launch(headless=headless, slow_mo=500)
            case "webkit":
                cls.__browser = plw.webkit.launch(headless=headless, slow_mo=500)
            case _:
                raise ValueError("Invalid Browser Type !!!")

    @classmethod
    def close_browser(cls):

        if cls.__context:
            logger.info(" [BrowserManager] Close context")
            cls.__context.close()

        if cls.__browser:
            logger.info(" [BrowserManager] Close browser")
            cls.__browser.close()

        if cls.__plw:
            logger.info(" [BrowserManager] Stop playwright")
            cls.__plw.stop()

    @classmethod
    def init_page(cls, browser_type="chrome", headless=False):
        if not cls.__browser:
            logger.info(" [BrowserManager] Create new browser")
            cls.init_browser(browser_type, headless)

        logger.info(" [BrowserManager] Create new context")
        cls.__context = cls.__browser.new_context()

        logger.info(" [BrowserManager] Create new page")
        cls.__page = cls.__context.new_page()

        return cls.__page

    @classmethod
    def get_page(cls):
        return cls.__page
