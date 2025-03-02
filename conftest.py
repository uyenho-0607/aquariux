import os

import allure
import pytest
from playwright.sync_api import Page

from src.base.browser_manager import BrowserManager
from src.consts import ROOTDIR
from src.pages_object.login_page import LoginPage
from src.utils import load_config_data
from src.utils.allure_utils import log_step_to_allure, custom_allure_report
from src.utils.logging_utils import logger, setup_logging


def pytest_addoption(parser):
    parser.addoption("--browser_type", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption("--env", action="store", choices=["qa", "staging"], default="qa")


def pytest_sessionstart(session):
    logger.info("============ pytest_sessionstart ============ ")
    setup_logging()
    config_data = load_config_data(session.config.getoption("env"))

    headless = session.config.getoption("headless")
    browser = session.config.getoption("browser_type")

    logger.info('-- Init page')
    page: Page = BrowserManager.init_page(browser, headless)
    page.goto(config_data["url"])

    logger.info('- Perform login')
    LoginPage(page).login(config_data["user_id"], config_data["password"])


def pytest_sessionfinish(session):
    logger.info("============ pytest_sessionfinish ============ ")
    BrowserManager.close_browser()

    allure_dir = session.config.option.allure_report_dir
    if allure_dir and os.path.exists(ROOTDIR / allure_dir):
        custom_allure_report(allure_dir)

        env_data = {
            "Environment": session.config.getoption("--env").capitalize()
        }

        with open(f"{allure_dir}/environment.properties", "w") as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Check if the report is from the 'call' phase
    if report.when == "call":
        log_step_to_allure()

        if report.failed:
            page = BrowserManager.get_page()
            screenshot = page.screenshot()
            allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
