"""Shared pytest fixtures: WebDriver setup/teardown and reusable test data."""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from pages.login_page import LoginPage

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PASSWORD = "secret_sauce"


@pytest.fixture
def driver():
    """Provides a Chrome WebDriver instance, headless by default for CI."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1400,1000")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    yield drv
    drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Provides a WebDriver already logged in as the standard user."""
    login_page = LoginPage(driver).load()
    login_page.login(STANDARD_USER, PASSWORD)
    return driver
