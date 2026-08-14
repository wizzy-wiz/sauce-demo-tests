"""AI-assisted test failure triage.

Reads a pytest JSON report (generated with the pytest-json-report plugin)
and, for each failed test, asks an LLM to produce a short human-readable
summary: likely root-cause category, a plain-English explanation, and a
draft ticket description ready to paste into Jira/Confluence.

This mirrors real work: at In-tech, failed TestGuide runs are reviewed
manually to write up tickets and route them to the right team. This script
automates the first pass of that triage — a human still reviews and
assigns, but doesn't start from a blank page for every failure.

Usage:
    pytest --json-report --json-report-file=report.json
    python scripts/ai_failure_summarizer.py report.json

Requires an ANTHROPIC_API_KEY environment variable. Without one, the
script runs in demo mode and prints a sample summary so the output format
is visible without needing an API key.
"""

import json
import os
import sys

DEMO_FAILURE = {
    "nodeid": "tests/test_cart.py::test_add_single_item_updates_cart_badge",
    "longrepr": (
        "AssertionError: assert 0 == 1\n"
        " +  where 0 = get_cart_count()\n"
        "selenium.common.exceptions.NoSuchElementException: "
        "Unable to locate element: [id=\"add-to-cart-sauce-labs-backpack\"]"
    ),
}


def build_prompt(test_id: str, traceback_text: str) -> str:
    return f"""A pytest test failed. Analyze the failure and respond in this exact format:

CATEGORY: <one of: Locator changed, Timing/flaky, Environment issue, Real regression, Test data issue>
SUMMARY: <one sentence, plain English>
TICKET DRAFT: <2-3 sentence draft ready to paste into a bug tracker, written for someone unfamiliar with this test>

Test: {test_id}
Traceback:
{traceback_text}
"""


def summarize_with_claude(test_id: str, traceback_text: str) -> str:
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": build_prompt(test_id, traceback_text)}],
    )
    return response.content[0].text


def run_demo_mode():
    print("No ANTHROPIC_API_KEY found — running in demo mode with a sample failure.\n")
    print(f"Test: {DEMO_FAILURE['nodeid']}")
    print("-" * 70)
    print("CATEGORY: Locator changed")
    print(
        "SUMMARY: The 'Add to cart' button's element ID no longer matches "
        "what the test expects, so Selenium can't find it to click."
    )
    print(
        "TICKET DRAFT: test_add_single_item_updates_cart_badge fails because "
        "the add-to-cart button ID has changed on the inventory page. "
        "Likely a front-end markup change; update the locator in "
        "pages/inventory_page.py once the new ID is confirmed."
    )
    print("-" * 70)
    print("\n(This is a hardcoded example. With a real ANTHROPIC_API_KEY set, ")
    print("this same output is generated live from actual pytest failures.)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/ai_failure_summarizer.py <report.json>")
        print("(No report file given — showing demo mode instead.)\n")
        run_demo_mode()
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        run_demo_mode()
        return

    report_path = sys.argv[1]
    with open(report_path) as f:
        report = json.load(f)

    failed_tests = [t for t in report.get("tests", []) if t.get("outcome") == "failed"]

    if not failed_tests:
        print("No failed tests found in report — nothing to summarize.")
        return

    for test in failed_tests:
        test_id = test["nodeid"]
        traceback_text = test.get("call", {}).get("longrepr", "No traceback available.")
        print(f"Test: {test_id}")
        print("-" * 70)
        print(summarize_with_claude(test_id, traceback_text))
        print("-" * 70)
        print()


if __name__ == "__main__":
    main()
