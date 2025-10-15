import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.form_fields_page import FormFieldsPage
import allure

@pytest.fixture
def driver():
    """Фикстура для инициализации драйвера"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Новый headless режим
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver
    driver.quit()

@pytest.fixture
def form_page(driver):
    """Фикстура для страницы с формой"""
    page = FormFieldsPage(driver)
    page.open("https://practice-automation.com/form-fields/")
    return page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншотов при падении тестов"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_failure",
                attachment_type=allure.attachment_type.PNG
            )

@pytest.fixture(autouse=True)
def take_screenshot_on_success(request, driver):
    """Фикстура для скриншотов успешных тестов"""
    yield
    if request.node.rep_call.passed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name="screenshot_success",
            attachment_type=allure.attachment_type.PNG
        )