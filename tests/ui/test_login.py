import pytest
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage

@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.open()
    return page

def test_valid_login(login_page, driver):
    print("\nValidando login exitoso con 'standard_user'...")
    login_page.login("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(driver)
    print("Validando que la pagina de inventario este visible...")
    assert inventory_page.is_inventory_displayed()

def test_locked_out_user(login_page):
    print("\nValidando login con usuario bloqueado 'locked_out_user'...")
    login_page.login("locked_out_user", "secret_sauce")
    print("Validando que el mensaje de error sea el esperado para usuario bloqueado...")
    assert "Epic sadface: Sorry, this user has been locked out." in login_page.get_error_message()

def test_invalid_login(login_page):
    print("\nValidando login con credenciales invalidas...")
    login_page.login("invalid_user", "wrong_password")
    print("Validando que el mensaje de error sea el esperado para credenciales incorrectas...")
    assert "Epic sadface: Username and password do not match any user in this service" in login_page.get_error_message()
