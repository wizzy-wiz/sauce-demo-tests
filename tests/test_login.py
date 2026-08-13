"""Test suite: login flows on the Sauce Demo site.

Covers the standard positive path plus common negative/edge cases,
mirroring the kind of coverage expected in a real regression suite.
"""

import pytest

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from tests.conftest import STANDARD_USER, LOCKED_OUT_USER, PASSWORD


def test_successful_login_shows_inventory(driver):
    login_page = LoginPage(driver).load()
    login_page.login(STANDARD_USER, PASSWORD)

    inventory_page = InventoryPage(driver)
    assert inventory_page.is_loaded()
    assert inventory_page.item_count() == 6


def test_locked_out_user_sees_error(driver):
    login_page = LoginPage(driver).load()
    login_page.login(LOCKED_OUT_USER, PASSWORD)

    assert "locked out" in login_page.get_error_message().lower()


@pytest.mark.parametrize(
    "username,password,expected_snippet",
    [
        ("", "", "username is required"),
        (STANDARD_USER, "", "password is required"),
        ("not_a_real_user", "wrong_password", "do not match"),
    ],
)
def test_invalid_login_combinations(driver, username, password, expected_snippet):
    login_page = LoginPage(driver).load()
    login_page.login(username, password)

    assert expected_snippet in login_page.get_error_message().lower()
