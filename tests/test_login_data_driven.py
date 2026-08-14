"""Data-driven version of the invalid-login test in test_login.py.

Instead of hardcoding test cases in the test file, cases are read from
data/login_test_data.csv — adding a new scenario means adding a row to the
CSV, not touching the test code. This mirrors how larger regression suites
keep test data separate from test logic so non-developers (e.g. QA leads)
can extend coverage without editing Python.
"""

import csv
import os

import pytest

from pages.login_page import LoginPage

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "login_test_data.csv")


def load_login_cases():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [
            (row["username"], row["password"], row["expected_error_snippet"])
            for row in reader
        ]


@pytest.mark.parametrize("username,password,expected_snippet", load_login_cases())
def test_invalid_login_from_csv(driver, username, password, expected_snippet):
    login_page = LoginPage(driver).load()
    login_page.login(username, password)

    assert expected_snippet in login_page.get_error_message().lower()
