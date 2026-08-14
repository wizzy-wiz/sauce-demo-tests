"""Test suite: login flows on the Sauce Demo site.

Covers the standard positive path plus common negative/edge cases,
mirroring the kind of coverage expected in a real regression suite.
"""

import allure
import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from tests.conftest import STANDARD_USER, LOCKED_OUT_USER, PASSWORD


@allure.feature("Login")
@allure.title("Standard user can log in and sees the product inventory")
def test_successful_login_shows_inventory(driver):
    with allure.step("Log in as standard_user"):
        login_page = LoginPage(driver).load()
        login_page.login(STANDARD_USER, PASSWORD)

    with allure.step("Verify inventory page loaded with 6 products"):
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_loaded()
        assert inventory_page.item_count() == 6


@allure.feature("Login")
@allure.title("Locked-out user sees an error message")
def test_locked_out_user_sees_error(driver):
    with allure.step("Attempt login as locked_out_user"):
        login_page = LoginPage(driver).load()
        login_page.login(LOCKED_OUT_USER, PASSWORD)

    with allure.step("Verify error message is shown"):
        assert "locked out" in login_page.get_error_message().lower()


# Invalid-login scenarios (empty fields, wrong password, etc.) are covered by
# the data-driven version in test_login_data_driven.py, which reads its cases
# from data/login_test_data.csv instead of hardcoding them here.
