import csv
import pathlib
import pytest
from tests.pages.login_page import LoginPage
from tests.pages.inventory_page import InventoryPage


def load_login_data():
    """Lee los casos de prueba de login desde tests/data/login_data.csv."""
    data_file = pathlib.Path(__file__).parent.parent / "data" / "login_data.csv"
    cases = []
    with open(data_file, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cases.append((
                row["username"],
                row["password"],
                row["should_login"].lower() == "true",
                row["expected_error"],
            ))
    return cases

@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.open()
    return page

@pytest.mark.ui
def test_valid_login(login_page, driver):
    print("\nValidando login exitoso con 'standard_user'...")
    login_page.login("standard_user", "secret_sauce")
    
    inventory_page = InventoryPage(driver)
    print("Validando que la pagina de inventario este visible...")
    assert inventory_page.is_inventory_displayed()

@pytest.mark.ui
def test_locked_out_user(login_page):
    print("\nValidando login con usuario bloqueado 'locked_out_user'...")
    login_page.login("locked_out_user", "secret_sauce")
    print("Validando que el mensaje de error sea el esperado para usuario bloqueado...")
    assert "Epic sadface: Sorry, this user has been locked out." in login_page.get_error_message()

@pytest.mark.ui
def test_invalid_login(login_page):
    print("\nValidando login con credenciales invalidas...")
    login_page.login("invalid_user", "wrong_password")
    print("Validando que el mensaje de error sea el esperado para credenciales incorrectas...")
    assert "Epic sadface: Username and password do not match any user in this service" in login_page.get_error_message()


@pytest.mark.ui
@pytest.mark.parametrize("username,password,should_login,expected_error", load_login_data())
def test_login_parametrizado(login_page, driver, username, password, should_login, expected_error):
    """Ejecuta casos de login leídos desde tests/data/login_data.csv."""
    print(f"\nCaso parametrizado — usuario: '{username}', debe_loguear: {should_login}")
    login_page.login(username, password)
    if should_login:
        assert InventoryPage(driver).is_inventory_displayed()
    else:
        assert expected_error in login_page.get_error_message()
