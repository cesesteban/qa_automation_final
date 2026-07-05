import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os

@pytest.fixture(scope="function")
def driver(request):
    """
    Initializes the WebDriver instance for each test.
    Supports running in headless mode if specified via environment variables.
    """
    options = webdriver.ChromeOptions()
    
    # Check if headless mode is requested
    if os.environ.get("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    
    # Initialize driver using webdriver-manager
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Maximize window and set implicit wait
    driver.maximize_window()
    driver.implicitly_wait(5)
    
    yield driver
    
    # Take screenshot on failure before quitting
    if request.node.rep_call.failed:
        # Create screenshots directory if it doesn't exist
        os.makedirs("screenshots", exist_ok=True)
        screenshot_name = f"screenshots/{request.node.name}.png"
        driver.save_screenshot(screenshot_name)
        print(f"Screenshot saved to {screenshot_name}")
        
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test execution status.
    This allows the driver fixture to know if a test failed.
    """
    outcome = yield
    rep = outcome.get_result()
    # Set an attribute for each phase of a call, which can be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)
