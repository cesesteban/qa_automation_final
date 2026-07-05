from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage

class InventoryPage(BasePage):
    # Locators
    TITLE = (By.CSS_SELECTOR, "span.title")
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    FIRST_PRODUCT_NAME = (By.CSS_SELECTOR, ".inventory_item:first-child .inventory_item_name")
    FIRST_PRODUCT_PRICE = (By.CSS_SELECTOR, ".inventory_item:first-child .inventory_item_price")
    SORT_FILTER = (By.CLASS_NAME, "product_sort_container")
    
    # Social Media Links
    TWITTER_LINK = (By.CSS_SELECTOR, ".social_twitter a")
    FACEBOOK_LINK = (By.CSS_SELECTOR, ".social_facebook a")
    LINKEDIN_LINK = (By.CSS_SELECTOR, ".social_linkedin a")
    
    def __init__(self, driver):
        super().__init__(driver)

    def is_inventory_displayed(self):
        is_title_correct = self.is_visible(self.TITLE) and self.get_text(self.TITLE) == "Products"
        is_logo_correct = self.is_visible(self.APP_LOGO) and self.get_text(self.APP_LOGO) == "Swag Labs"
        is_url_correct = "/inventory.html" in self.driver.current_url
        
        return is_title_correct and is_logo_correct and is_url_correct

    def add_item_to_cart(self, item_id):
        # item_id is something like 'add-to-cart-sauce-labs-backpack'
        locator = (By.ID, item_id)
        self.js_click(locator)

    def remove_item_from_cart(self, item_id):
        # item_id is something like 'remove-sauce-labs-backpack'
        locator = (By.ID, item_id)
        self.js_click(locator)

    def get_cart_count(self):
        import time
        time.sleep(0.5)
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def are_products_displayed(self):
        # Usar find_elements para contar la cantidad de productos
        from selenium.webdriver.support import expected_conditions as EC
        try:
            products = self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_ITEMS))
            return len(products) > 0
        except:
            return False

    def get_first_product_details(self):
        name = self.get_text(self.FIRST_PRODUCT_NAME)
        price = self.get_text(self.FIRST_PRODUCT_PRICE)
        return name, price

    def are_ui_elements_present(self):
        return self.is_visible(self.HAMBURGER_MENU_BTN) and self.is_visible(self.SORT_FILTER)

    def get_social_link(self, platform):
        """Devuelve el atributo href del enlace de la red social especificada."""
        locators = {
            "twitter": self.TWITTER_LINK,
            "facebook": self.FACEBOOK_LINK,
            "linkedin": self.LINKEDIN_LINK
        }
        element = self.find_element(locators[platform.lower()])
        return element.get_attribute("href")

    def click_social_link(self, platform):
        """Hace clic en el enlace de la red social especificada."""
        locators = {
            "twitter": self.TWITTER_LINK,
            "facebook": self.FACEBOOK_LINK,
            "linkedin": self.LINKEDIN_LINK
        }
        self.click(locators[platform.lower()])
