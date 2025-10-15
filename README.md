# Form Automation Project

Проект автоматизации тестирования формы на сайте practice-automation.com

## Тест-кейс

**Предусловие:**
1. Открыть браузер
2. Перейти по ссылке https://practice-automation.com/form-fields/

**Шаги:**
1. Заполнить поле Name
2. Заполнить поле Password
3. Из списка What is your favorite drink? выбрать Milk и Coffee
4. Из списка What is your favorite color? выбрать Yellow
5. В поле Do you like automation? выбрать любой вариант
6. Поле Email заполнить строкой формата name@example.com

## Запуск тестов

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest

# Запуск с Allure отчетами
pytest --alluredir=allure-results
allure serve allure-results

# Запуск только smoke тестов
pytest -m smoke

# Запуск с HTML отчетом
pytest --html=report.html