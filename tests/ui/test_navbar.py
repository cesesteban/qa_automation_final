import pytest
import time
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage

@pytest.fixture
def inventory_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    return InventoryPage(driver)

def test_navbar_all_items(inventory_page, driver):
    """Valida que el botón 'All Items' redirija a la página de inventario."""
    print("\nNavegando a 'All Items' desde el carrito...")
    driver.get("https://www.saucedemo.com/cart.html")
    
    inventory_page.go_to_all_items()
    
    assert "/inventory.html" in driver.current_url
    assert inventory_page.is_inventory_displayed()
    print("-> Redirección a 'All Items' exitosa.")

def test_navbar_about(inventory_page, driver):
    """Valida que el botón 'About' redirija al sitio web de Sauce Labs."""
    print("\nNavegando a 'About'...")
    inventory_page.go_to_about()
    
    # Validar que la URL contenga saucelabs.com
    assert "saucelabs.com" in driver.current_url
    print(f"-> Redirección a 'About' exitosa: {driver.current_url}")

def test_navbar_logout(inventory_page, driver):
    """Valida que el botón 'Logout' cierre la sesión correctamente."""
    print("\nEjecutando Logout...")
    inventory_page.logout()
    
    # Validar que redirija a la página de login
    assert "www.saucedemo.com" in driver.current_url
    # Verificar que el botón de login sea visible (estamos fuera)
    login_page = LoginPage(driver)
    assert login_page.is_visible(login_page.LOGIN_BUTTON)
    print("-> Logout exitoso.")

def test_navbar_reset_app_state(inventory_page, driver):
    """Valida que 'Reset App State' limpie el estado de la aplicación (ej. el carrito)."""
    print("\nAgregando producto y reseteando estado...")
    inventory_page.add_item_to_cart("add-to-cart-sauce-labs-backpack")
    assert inventory_page.get_cart_count() == 1
    
    inventory_page.reset_app_state()
    time.sleep(1) # Darle tiempo a la limpieza de localStorage
    
    # En Saucedemo el badge desaparece al resetear
    assert inventory_page.get_cart_count() == 0
    print("-> Reset App State exitoso (carrito vacío).")
