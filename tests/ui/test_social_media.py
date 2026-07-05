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

def test_social_links_visibility(inventory_page):
    """Valida que los 3 botones de redes sociales sean visibles en la página."""
    print("\nValidando visibilidad de redes sociales...")
    assert inventory_page.is_visible(inventory_page.TWITTER_LINK), "Twitter link no es visible"
    assert inventory_page.is_visible(inventory_page.FACEBOOK_LINK), "Facebook link no es visible"
    assert inventory_page.is_visible(inventory_page.LINKEDIN_LINK), "LinkedIn link no es visible"
    print("-> Todos los botones son visibles.")

def test_social_links_urls(inventory_page):
    """Valida que los enlaces de redes sociales apunten a las URLs correctas."""
    print("\nValidando URLs de redes sociales...")
    
    expected_links = {
        "twitter": "https://twitter.com/saucelabs",
        "facebook": "https://www.facebook.com/saucelabs",
        "linkedin": "https://www.linkedin.com/company/sauce-labs/"
    }
    
    for platform, expected_url in expected_links.items():
        actual_url = inventory_page.get_social_link(platform)
        print(f"-> {platform.capitalize()}: {actual_url}")
        assert actual_url == expected_url, f"La URL de {platform} no coincide. Esperado: {expected_url}, Obtenido: {actual_url}"

def test_social_links_navigation(inventory_page, driver):
    """Valida que al hacer clic se abra una nueva pestaña con la URL correcta."""
    print("\nValidando navegación a Twitter...")
    
    # Guardar el identificador de la ventana actual
    original_window = driver.current_window_handle
    
    inventory_page.click_social_link("twitter")
    time.sleep(2) # Esperar a que se abra la pestaña
    
    # Obtener todos los identificadores de ventana
    all_windows = driver.window_handles
    
    # Cambiar a la nueva pestaña
    for window in all_windows:
        if window != original_window:
            driver.switch_to.window(window)
            break
            
    print(f"-> URL en nueva pestaña: {driver.current_url}")
    assert "twitter.com/saucelabs" in driver.current_url.lower() or "x.com/saucelabs" in driver.current_url.lower()
    
    # Cerrar pestaña y volver a la original
    driver.close()
    driver.switch_to.window(original_window)
