from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from typing import List, Tuple

class BasePage:
    """Базовый класс для всех страниц с реализацией Fluent Interface"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """Найти элемент с ожиданием"""
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Найти элементы с ожиданием"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click(self, locator: Tuple[str, str]) -> 'BasePage':
        """Кликнуть по элементу (Fluent interface)"""
        element = self.find_element(locator)
        element.click()
        return self
    
    def type_text(self, locator: Tuple[str, str], text: str) -> 'BasePage':
        """Ввести текст в поле (Fluent interface)"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return self
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Получить текст элемента"""
        return self.find_element(locator).text
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Проверить наличие элемента"""
        try:
            self.find_element(locator)
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, filename: str) -> 'BasePage':
        """Сделать скриншот (Fluent interface)"""
        self.driver.save_screenshot(filename)
        return self
    
    def open(self, url: str) -> 'BasePage':
        """Открыть URL (Fluent interface)"""
        self.driver.get(url)
        return self