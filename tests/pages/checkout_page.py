from selenium.webdriver.common.by import By
from tests.pages.base_page import BasePage

class CheckoutPage(BasePage):
    # Locators - Step One (Your Information)
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    
    # Locators - Step Two (Overview)
    FINISH_BUTTON = (By.ID, "finish")
    SUMMARY_TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    
    # Locators - Complete
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    TITLE = (By.CSS_SELECTOR, "span.title")
    
    def __init__(self, driver):
        super().__init__(driver)

    # Step One actions
    def is_checkout_step_one_displayed(self):
        try:
            from selenium.webdriver.support import expected_conditions as EC
            self.wait.until(EC.url_contains("/checkout-step-one.html"))
            return True
        except:
            return False

    def fill_information_and_continue(self, first_name, last_name, postal_code):
        import time
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        self.type_text(self.LAST_NAME_INPUT, last_name)
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        time.sleep(1) # Sincronización con React
        element = self.find_element(self.CONTINUE_BUTTON)
        element.submit()

    # Step Two actions
    def is_checkout_step_two_displayed(self):
        try:
            from selenium.webdriver.support import expected_conditions as EC
            self.wait.until(EC.url_contains("/checkout-step-two.html"))
            return True
        except:
            return False
        
    def get_summary_total(self):
        return self.get_text(self.SUMMARY_TOTAL_LABEL)
        
    def get_items_count(self):
        try:
            from selenium.webdriver.support import expected_conditions as EC
            items = self.wait.until(EC.presence_of_all_elements_located(self.CART_ITEMS))
            return len(items)
        except:
            return 0

    def finish_checkout(self):
        self.click(self.FINISH_BUTTON)

    # Complete actions
    def is_checkout_complete_displayed(self):
        try:
            from selenium.webdriver.support import expected_conditions as EC
            self.wait.until(EC.url_contains("/checkout-complete.html"))
            return True
        except:
            return False
        
    def get_complete_message(self):
        return self.get_text(self.COMPLETE_HEADER)
