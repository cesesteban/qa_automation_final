import os
import pytest
from datetime import datetime
from selenium import webdriver
from utils.logger import logger


@pytest.fixture(scope="function")
def driver(request):
    """Inicializa el WebDriver para cada test. Soporta modo headless via variable de entorno HEADLESS=true."""
    options = webdriver.ChromeOptions()

    if os.environ.get("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

    # Opciones requeridas en entornos CI/contenedores
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Selenium Manager (integrado en Selenium 4.6+) gestiona ChromeDriver automáticamente
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(5)

    logger.info(f"Iniciando test: {request.node.name}")

    yield driver

    # Captura screenshot con timestamp si el test falló
    if request.node.rep_call.failed:
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"screenshots/{timestamp}_{request.node.name}.png"
        driver.save_screenshot(screenshot_name)
        logger.error(f"Test FALLIDO — screenshot guardado: {screenshot_name}")
        print(f"Screenshot guardado: {screenshot_name}")

    logger.info(f"Finalizando test: {request.node.name}")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar el estado de ejecución de cada test y hacerlo accesible al fixture driver."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
