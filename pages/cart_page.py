"""Page Object for the Sauce Demo cart page."""

from selenium.webdriver.common.by import By


class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button.cart_button")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def get_item_names(self) -> list[str]:
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def remove_first_item(self):
        self.driver.find_elements(*self.REMOVE_BUTTONS)[0].click()

    def go_to_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BUTTON).click()
