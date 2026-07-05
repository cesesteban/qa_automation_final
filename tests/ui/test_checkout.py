import pytest
import time
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage
from tests.pages.cart_page import CartPage
from tests.pages.checkout_page import CheckoutPage

@pytest.fixture
def logged_in_inventory_page(driver):
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(driver)
    return inventory_page

def test_e2e_shopping_flow(logged_in_inventory_page, driver):
    inventory_page = logged_in_inventory_page
    
    print("\n--- PASO 1: Agregar 3 productos al carrito ---")
    inventory_page.add_item_to_cart("add-to-cart-sauce-labs-backpack")
    inventory_page.add_item_to_cart("add-to-cart-sauce-labs-bike-light")
    inventory_page.add_item_to_cart("add-to-cart-sauce-labs-bolt-t-shirt")
    
    time.sleep(1) # Esperar a que el badge de la UI se actualice
    assert inventory_page.get_cart_count() == 3
    
    print("Navegando al carrito...")
    driver.get("https://www.saucedemo.com/cart.html")
    
    cart_page = CartPage(driver)
    print("Validando carrito...")
    assert cart_page.is_cart_displayed()
    assert cart_page.get_cart_items_count() == 3
    
    print("\n--- PASO 2: 'Editar' cantidades (Remover 1 producto) ---")
    # En Saucedemo solo podemos remover para simular edición de carrito
    cart_page.remove_first_item()
    time.sleep(1) # Esperar actualización del badge/lista
    assert cart_page.get_cart_items_count() == 2
    
    print("\n--- PASO 3: Proceso de Checkout ---")
    cart_page.go_to_checkout()
    
    checkout_page = CheckoutPage(driver)
    assert checkout_page.is_checkout_step_one_displayed()
    
    print("Llenando formulario de informacion...")
    time.sleep(1) # Esperar a que React asiente la vista y no borre los inputs
    checkout_page.fill_information_and_continue("John", "Doe", "12345")
    
    if not checkout_page.is_checkout_step_two_displayed():
        print('URL ACTUAL:', driver.current_url)
        print('PAGE SOURCE:', driver.page_source[:1000])
    assert checkout_page.is_checkout_step_two_displayed()
    
    print("Validando Overview...")
    assert checkout_page.get_items_count() == 2
    total_label = checkout_page.get_summary_total()
    print(f"-> Total verificado: {total_label}")
    
    print("Finalizando la compra...")
    checkout_page.finish_checkout()
    
    print("\n--- PASO 4: Validacion final ---")
    assert checkout_page.is_checkout_complete_displayed()
    message = checkout_page.get_complete_message()
    print(f"-> Mensaje final de éxito: {message}")
    assert message == "Thank you for your order!"
