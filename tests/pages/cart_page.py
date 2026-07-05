from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage

class CartPage(BasePage):
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    TITLE = (By.CSS_SELECTOR, "span.title")
    
    def __init__(self, driver):
        super().__init__(driver)

    def is_cart_displayed(self):
        try:
            from selenium.webdriver.support import expected_conditions as EC
            self.wait.until(EC.url_contains("/cart.html"))
            return True
        except:
            return False

    def get_cart_items_count(self):
        import time
        time.sleep(0.5)
        try:
            from selenium.webdriver.support import expected_conditions as EC
            items = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
            return len(items)
        except:
            return 0

    def remove_item(self, item_id):
        # item_id example: 'remove-sauce-labs-backpack'
        locator = (By.ID, item_id)
        self.click(locator)
        
    def remove_first_item(self):
        from selenium.webdriver.common.by import By
        import time
        # Utilizamos js_click ya que los botones de remover en Saucedemo a veces fallan silenciosamente
        self.js_click((By.XPATH, "(//button[text()='Remove'])[1]"))
        time.sleep(1)

    def go_to_checkout(self):
        self.js_click(self.CHECKOUT_BUTTON)
