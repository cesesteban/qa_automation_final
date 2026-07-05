import pytest
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage

@pytest.fixture
def logged_in_inventory_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(driver)
    return inventory_page

def test_add_item_to_cart(logged_in_inventory_page):
    page = logged_in_inventory_page
    
    # Assert cart is initially empty
    assert page.get_cart_count() == 0
    
    # Add an item to the cart
    page.add_item_to_cart("add-to-cart-sauce-labs-backpack")
    
    # Assert cart count is 1
    assert page.get_cart_count() == 1

def test_remove_item_from_cart(logged_in_inventory_page):
    page = logged_in_inventory_page
    
    # Add an item first
    page.add_item_to_cart("add-to-cart-sauce-labs-backpack")
    assert page.get_cart_count() == 1
    
    # Remove the item
    page.remove_item_from_cart("remove-sauce-labs-backpack")
    
    # Assert cart is empty
    assert page.get_cart_count() == 0

def test_inventory_navigation(logged_in_inventory_page):
    page = logged_in_inventory_page
    
    print("\nValidando que el titulo de la pagina de inventario sea correcto...")
    assert page.is_inventory_displayed()
    
    print("Comprobando que existan productos visibles en la pagina...")
    assert page.are_products_displayed()
    
    print("Listando nombre/precio del primero...")
    name, price = page.get_first_product_details()
    print(f"-> Primer producto: '{name}' - Precio: '{price}'")
    assert name != "" and price != ""
    
    print("Validando que elementos importantes de la interfaz esten presentes (menu, filtros)...")
    assert page.are_ui_elements_present()
