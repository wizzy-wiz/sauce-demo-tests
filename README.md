# Sauce Demo – Test Automation Portfolio

A Python test automation project built around [saucedemo.com](https://www.saucedemo.com/), a public demo e-commerce site used industry-wide for practicing test automation. Started as a UI test suite and expanded into a small but complete demonstration of the tools and practices used in professional test automation roles: UI testing, API testing, data-driven testing, keyword-driven testing (Robot Framework), AI-assisted failure triage, and CI pipelines across three different platforms.

## What it tests

- **UI — Login flows** (`tests/test_login.py`) — successful login, locked-out user
- **UI — Login flows, data-driven** (`tests/test_login_data_driven.py`) — invalid-input scenarios read from `data/login_test_data.csv`, so new cases can be added without touching test code
- **UI — Cart flows** (`tests/test_cart.py`) — adding single/multiple items, cart badge count, removing items, price sorting
- **API** (`tests_api/test_jsonplaceholder_api.py`) — GET/POST/PATCH/DELETE against [JSONPlaceholder](https://jsonplaceholder.typicode.com/), a public fake REST API — no browser involved, tests the HTTP layer directly
- **Keyword-driven (Robot Framework)** (`robot/login_tests.robot`) — the two core login scenarios re-implemented in Robot Framework syntax, to demonstrate that style of automation alongside the pytest suite
- **AI-assisted failure triage** (`scripts/ai_failure_summarizer.py`) — summarizes pytest failures using Claude, drafting a root-cause category and ticket description automatically

## Structure

```
sauce-demo-tests/
├── pages/                  # Page Object Model — one class per page, no test logic
│   ├── login_page.py
│   ├── inventory_page.py
│   └── cart_page.py
├── tests/
│   ├── conftest.py         # WebDriver fixtures (headless Chrome, auto setup/teardown)
│   ├── test_login.py
│   ├── test_login_data_driven.py
│   └── test_cart.py
├── tests_api/
│   └── test_jsonplaceholder_api.py
├── data/
│   └── login_test_data.csv # test cases for the data-driven login test
├── robot/
│   └── login_tests.robot   # Robot Framework demo
├── scripts/
│   └── ai_failure_summarizer.py  # AI-assisted failure triage (Claude API)
├── .github/workflows/tests.yml   # GitHub Actions — active CI on this repo
├── .gitlab-ci.yml                # GitLab CI config
├── Jenkinsfile                   # Jenkins declarative pipeline
└── requirements.txt
```

## Why Page Object Model

Each page of the site has its own class holding its locators and actions. Tests read like plain English (`inventory_page.add_first_item_to_cart()`) and don't know or care about CSS selectors. If the site's HTML changes, only the page object needs updating — not every test that touches that page.

## Why a separate CSV-driven test

`test_login.py` covers the "happy path" and one clear negative case directly in code. `test_login_data_driven.py` covers a broader set of invalid-input combinations by reading them from `data/login_test_data.csv` instead — adding a new scenario means adding a row to the CSV, not editing Python. This mirrors how larger regression suites separate test data from test logic so test cases can be extended by anyone on the team, not just whoever wrote the framework.

## Running locally

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

pytest                                              # run all UI + API tests
pytest --html=report.html --self-contained-html     # with an HTML report
pytest --alluredir=allure-results                   # generate Allure results (see below)

python -m robot robot/login_tests.robot             # run the Robot Framework demo
```

Chrome is required for the UI tests; [webdriver-manager](https://pypi.org/project/webdriver-manager/) downloads the matching ChromeDriver automatically. The API tests need no browser at all.

## AI-assisted failure triage

`scripts/ai_failure_summarizer.py` reads a pytest JSON report and asks an LLM (Anthropic's Claude, via the `anthropic` package) to summarize each failure: a likely root-cause category, a plain-English explanation, and a draft ticket description. This automates the first pass of the same triage done manually in the In-tech role above — reviewing failed runs, writing up what went wrong, and preparing a ticket — without needing to start from a blank page for every failure.

```bash
pytest --json-report --json-report-file=report.json
python scripts/ai_failure_summarizer.py report.json
```

No API key is required to see how it works — without `ANTHROPIC_API_KEY` set, it runs in a demo mode that prints a realistic sample summary so the output format is visible immediately. With a real key, it generates the same kind of summary live from actual failures.

## Allure reports

This project uses [Allure](https://allurereport.org/) for richer, more readable test reports than plain pytest-html — step-by-step breakdowns, feature/story tagging, and a searchable history across runs.

```bash
pytest --alluredir=allure-results
allure serve allure-results     # opens the report in your browser
```

`allure serve` requires the Allure command-line tool (separate from the `allure-pytest` Python package already in `requirements.txt`) — install via `brew install allure` (Mac), `scoop install allure` (Windows), or see the [Allure installation docs](https://allurereport.org/docs/install/).

## Continuous Integration

This repo includes working pipeline configuration for **three** CI systems:

- **GitHub Actions** (`.github/workflows/tests.yml`) — active on this repo. Every push to `main` installs dependencies, runs the UI + API suite headlessly, generates the HTML and Allure reports, runs the Robot Framework demo, and publishes all of it as build artifacts.
- **GitLab CI** (`.gitlab-ci.yml`) — ready to run if this repo is mirrored or pushed to GitLab; GitLab picks the file up automatically.
- **Jenkins** (`Jenkinsfile`) — a declarative pipeline ready to be pointed at from a Jenkins "Pipeline script from SCM" job.

Since this repo is hosted on GitHub, only the GitHub Actions pipeline runs automatically today — the GitLab and Jenkins files are included as working, correct configuration to demonstrate familiarity with those platforms, not as claims that they're currently executing.

## Possible extensions

- Migrate the UI tests to [Playwright](https://playwright.dev/python/) for faster, more reliable browser automation
- Parallelize test execution with `pytest-xdist`
- Add contract testing between the API tests and a real backend schema
