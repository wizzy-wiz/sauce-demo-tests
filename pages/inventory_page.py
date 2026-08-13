"""Page Object for the Sauce Demo inventory (product listing) page."""

from selenium.webdriver.common.by import By


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button.btn_inventory")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")

    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self) -> bool:
        return self.driver.find_element(*self.PAGE_TITLE).text == "Products"

    def item_count(self) -> int:
        return len(self.driver.find_elements(*self.INVENTORY_ITEMS))

    def add_first_item_to_cart(self):
        self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)[0].click()

    def add_n_items_to_cart(self, n: int):
        buttons = self.driver.find_elements(*self.ADD_TO_CART_BUTTONS)
        for button in buttons[:n]:
            button.click()

    def get_cart_count(self) -> int:
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        self.driver.find_element(*self.CART_LINK).click()

    def sort_by(self, option_value: str):
        from selenium.webdriver.support.ui import Select
        Select(self.driver.find_element(*self.SORT_DROPDOWN)).select_by_value(option_value)

    def get_prices(self) -> list[float]:
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(e.text.replace("$", "")) for e in elements]
