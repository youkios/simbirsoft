from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .base_page import BasePage

class FormFieldsPage(BasePage):
    """Page Object для страницы с полями формы"""
    
    # Локаторы с использованием разных селекторов
    NAME_FIELD = (By.ID, "name")  # ID селектор
    PASSWORD_FIELD = (By.CSS_SELECTOR, "input[type='password']")  # CSS селектор
    EMAIL_FIELD = (By.XPATH, "//input[@type='email']")  # XPath селектор
    
    # Checkboxes для напитков
    DRINK_MILK = (By.CSS_SELECTOR, "input[value='Milk']")
    DRINK_COFFEE = (By.XPATH, "//input[@value='Coffee']")
    
    # Dropdown для цвета
    COLOR_DROPDOWN = (By.ID, "color")
    
    # Radio buttons для автоматизации
    AUTOMATION_YES = (By.CSS_SELECTOR, "input[value='Yes']")
    AUTOMATION_NO = (By.XPATH, "//input[@value='No']")
    
    # Кнопка submit
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    
    # Сообщение об успехе
    SUCCESS_MESSAGE = (By.ID, "message")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
    
    def fill_name(self, name: str) -> 'FormFieldsPage':
        """Заполнить поле Name (Fluent interface)"""
        return self.type_text(self.NAME_FIELD, name)
    
    def fill_password(self, password: str) -> 'FormFieldsPage':
        """Заполнить поле Password (Fluent interface)"""
        return self.type_text(self.PASSWORD_FIELD, password)
    
    def fill_email(self, email: str) -> 'FormFieldsPage':
        """Заполнить поле Email (Fluent interface)"""
        return self.type_text(self.EMAIL_FIELD, email)
    
    def select_drinks(self, drinks: list) -> 'FormFieldsPage':
        """Выбрать напитки из списка (Fluent interface)"""
        for drink in drinks:
            if drink.lower() == "milk":
                self.click(self.DRINK_MILK)
            elif drink.lower() == "coffee":
                self.click(self.DRINK_COFFEE)
        return self
    
    def select_color(self, color: str) -> 'FormFieldsPage':
        """Выбрать цвет из dropdown (Fluent interface)"""
        dropdown = Select(self.find_element(self.COLOR_DROPDOWN))
        dropdown.select_by_visible_text(color)
        return self
    
    def select_automation_preference(self, preference: str) -> 'FormFieldsPage':
        """Выбрать предпочтение по автоматизации (Fluent interface)"""
        if preference.lower() == "yes":
            self.click(self.AUTOMATION_YES)
        elif preference.lower() == "no":
            self.click(self.AUTOMATION_NO)
        return self
    
    def submit_form(self) -> 'FormFieldsPage':
        """Отправить форму (Fluent interface)"""
        return self.click(self.SUBMIT_BUTTON)
    
    def get_success_message(self) -> str:
        """Получить сообщение об успехе"""
        return self.get_text(self.SUCCESS_MESSAGE)
    
    def is_success_message_displayed(self) -> bool:
        """Проверить отображение сообщения об успехе"""
        return self.is_element_present(self.SUCCESS_MESSAGE)
    
    def fill_complete_form(self, name: str, password: str, email: str, 
                          drinks: list, color: str, automation_pref: str) -> 'FormFieldsPage':
        """Заполнить всю форму одним методом (Fluent interface)"""
        return (self.fill_name(name)
                .fill_password(password)
                .fill_email(email)
                .select_drinks(drinks)
                .select_color(color)
                .select_automation_preference(automation_pref))