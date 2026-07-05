import pytest
from tests.pages.base_page import BasePage

def test_example_search(driver):
    # This is an example test to verify the setup
    page = BasePage(driver, base_url="https://www.example.com")
    page.open()
    
    # Assert title or specific element
    assert "Example Domain" in driver.title
