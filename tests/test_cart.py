"""Test suite: adding items to cart and verifying cart state."""

import pytest

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


def test_add_single_item_updates_cart_badge(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_first_item_to_cart()

    assert inventory_page.get_cart_count() == 1


@pytest.mark.parametrize("n_items", [2, 3, 6])
def test_add_multiple_items_updates_cart_badge(logged_in_driver, n_items):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_n_items_to_cart(n_items)

    assert inventory_page.get_cart_count() == n_items


def test_cart_page_lists_added_items(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_n_items_to_cart(2)
    inventory_page.open_cart()

    cart_page = CartPage(logged_in_driver)
    assert cart_page.item_count() == 2


def test_removing_item_updates_cart(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_n_items_to_cart(2)
    inventory_page.open_cart()

    cart_page = CartPage(logged_in_driver)
    cart_page.remove_first_item()

    assert cart_page.item_count() == 1


def test_price_sort_low_to_high_is_ascending(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.sort_by("lohi")

    prices = inventory_page.get_prices()
    assert prices == sorted(prices)
