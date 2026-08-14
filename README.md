# Sauce Demo – Automated UI Test Suite

A Python/Selenium test automation framework for [saucedemo.com](https://www.saucedemo.com/), a public demo e-commerce site built for practicing test automation.

Built to demonstrate a realistic, maintainable test automation setup: Page Object Model, pytest fixtures, parametrized test cases, HTML reporting, and a CI pipeline that runs the suite automatically on every push.

## What it tests

- **Login flows** — successful login, locked-out user, and multiple invalid input combinations (parametrized)
- **Cart flows** — adding single/multiple items, verifying the cart badge count, removing items, and validating price sorting

## Structure

```
sauce-demo-tests/
├── pages/              # Page Object Model — one class per page, no test logic
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── tests/
│   ├── conftest.py     # WebDriver fixtures (headless Chrome, auto setup/teardown)
│   ├── test_login.py
│   └── test_cart.py
├── .github/workflows/tests.yml   # CI: runs the suite on every push/PR
└── requirements.txt
```

## Why Page Object Model

Each page of the site has its own class holding its locators and actions. Tests read like plain English (`inventory_page.add_first_item_to_cart()`) and don't know or care about CSS selectors. If the site's HTML changes, only the page object needs updating — not every test that touches that page.

## Running locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

pytest                                          # run all tests
pytest --html=report.html --self-contained-html # run with an HTML report
```

Chrome is required; [webdriver-manager](https://pypi.org/project/webdriver-manager/) downloads the matching ChromeDriver automatically.

## Continuous Integration

This repo includes working pipeline configuration for **three** CI systems, to demonstrate the same test suite running across different tooling:

- **GitHub Actions** (`.github/workflows/tests.yml`) — active on this repo. Every push to `main` installs dependencies, runs the full suite headlessly, and publishes the HTML report as a build artifact.
- **GitLab CI** (`.gitlab-ci.yml`) — ready to run if this repo is mirrored or pushed to GitLab; GitLab picks the file up automatically.
- **Jenkins** (`Jenkinsfile`) — a declarative pipeline ready to be pointed at from a Jenkins "Pipeline script from SCM" job.

All three run the identical command (`pytest --html=report.html --self-contained-html`) — only the environment setup and artifact-publishing syntax differs between platforms.

## Possible extensions

- Migrate to [Playwright](https://playwright.dev/python/) for faster, more reliable browser automation
- Add API-level tests alongside the UI tests
- Parallelize test execution with `pytest-xdist`
