import pytest
import allure
import re

@allure.epic("Form Automation")
@allure.feature("Работа с полями и формами")
class TestFormFields:
    
    @allure.story("Заполнение всех полей формы")
    @allure.title("Полное заполнение формы с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Тест проверяет заполнение всех полей формы согласно требованиям:
    1. Заполнить поле Name
    2. Заполнить поле Password  
    3. Выбрать Milk и Coffee из списка напитков
    4. Выбрать Yellow из списка цветов
    5. Выбрать вариант в поле Do you like automation?
    6. Заполнить Email в правильном формате
    """)
    def test_complete_form_filling(self, form_page):
        """Тест полного заполнения формы"""
        
        with allure.step("Предусловие: Открыть страницу с формой"):
            allure.attach(form_page.driver.current_url, "URL страницы", allure.attachment_type.TEXT)
        
        with allure.step("Заполнить поле Name"):
            form_page.fill_name("Test User")
        
        with allure.step("Заполнить поле Password"):
            form_page.fill_password("securepassword123")
        
        with allure.step("Выбрать Milk и Coffee из списка напитков"):
            form_page.select_drinks(["Milk", "Coffee"])
        
        with allure.step("Выбрать Yellow из списка цветов"):
            form_page.select_color("Yellow")
        
        with allure.step("Выбрать Yes в поле Do you like automation?"):
            form_page.select_automation_preference("Yes")
        
        with allure.step("Заполнить поле Email в формате name@example.com"):
            form_page.fill_email("testuser@example.com")
        
        with allure.step("Отправить форму"):
            form_page.submit_form()
        
        with allure.step("Проверить успешное отправление формы"):
            assert form_page.is_success_message_displayed(), "Сообщение об успехе не отображается"
            success_message = form_page.get_success_message()
            assert "success" in success_message.lower() or "thank" in success_message.lower(), \
                f"Неожиданное сообщение: {success_message}"
    
    @allure.story("Валидация email формата")
    @allure.title("Проверка валидного формата email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_email_format_validation(self, form_page):
        """Тест проверки формата email"""
        
        test_email = "name@example.com"
        
        with allure.step(f"Ввести email в формате: {test_email}"):
            form_page.fill_email(test_email)
        
        with allure.step("Проверить что email принят без ошибок"):
            # Здесь можно добавить проверку валидации, если она есть на странице
            email_field = form_page.find_element(form_page.EMAIL_FIELD)
            entered_value = email_field.get_attribute("value")
            assert entered_value == test_email, f"Введенный email не совпадает: {entered_value}"
            
            # Проверка формата email регулярным выражением
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            assert re.match(email_pattern, test_email), f"Email {test_email} не соответствует формату"
    
    @allure.story("Выбор multiple напитков")
    @allure.title("Проверка выбора нескольких напитков")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multiple_drinks_selection(self, form_page):
        """Тест выбора нескольких напитков"""
        
        with allure.step("Выбрать напиток Milk"):
            form_page.click(form_page.DRINK_MILK)
            milk_checkbox = form_page.find_element(form_page.DRINK_MILK)
            assert milk_checkbox.is_selected(), "Checkbox Milk не выбран"
        
        with allure.step("Выбрать напиток Coffee"):
            form_page.click(form_page.DRINK_COFFEE)
            coffee_checkbox = form_page.find_element(form_page.DRINK_COFFEE)
            assert coffee_checkbox.is_selected(), "Checkbox Coffee не выбран"
        
        with allure.step("Проверить что оба напитка выбраны"):
            assert milk_checkbox.is_selected() and coffee_checkbox.is_selected(), \
                "Не все выбранные напитки отмечены"

@pytest.mark.parametrize("automation_pref", ["Yes", "No"])
@allure.epic("Form Automation")
@allure.feature("Параметризованные тесты")
class TestParameterizedForm:
    
    @allure.story("Разные варианты автоматизации")
    @allure.title("Тест с выбором автоматизации: {automation_pref}")
    def test_different_automation_preferences(self, form_page, automation_pref):
        """Параметризованный тест для разных вариантов автоматизации"""
        
        with allure.step(f"Выбрать вариант '{automation_pref}' для автоматизации"):
            form_page.select_automation_preference(automation_pref)
            
            if automation_pref == "Yes":
                radio_button = form_page.find_element(form_page.AUTOMATION_YES)
            else:
                radio_button = form_page.find_element(form_page.AUTOMATION_NO)
            
            assert radio_button.is_selected(), f"Radio button {automation_pref} не выбран"

@pytest.mark.smoke
@allure.epic("Form Automation")
@allure.feature("Smoke тесты")
class TestSmokeForm:
    
    @allure.story("Быстрое заполнение формы")
    @allure.title("Smoke test - быстрое заполнение формы")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_quick_form_fill(self, form_page):
        """Smoke test быстрого заполнения формы"""
        
        with allure.step("Быстро заполнить все обязательные поля"):
            (form_page.fill_name("Smoke Test")
             .fill_password("smokepass")
             .fill_email("smoke@test.com")
             .select_drinks(["Milk"])
             .select_color("Yellow")
             .select_automation_preference("Yes")
             .submit_form())
        
        with allure.step("Проверить базовую функциональность"):
            assert form_page.driver.current_url != "https://practice-automation.com/form-fields/", \
                "Не произошел переход после отправки формы"