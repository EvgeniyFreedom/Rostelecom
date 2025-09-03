import pytest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

# Загружаем переменные окружения
load_dotenv()

PHONE = os.getenv("PHONE")
INVALID_PASSWORD = "wrong_password123"  # Тестовый невалидный пароль

@pytest.mark.parametrize("phone,password", [
    (PHONE, INVALID_PASSWORD),
])
def test_login_by_phone_invalid_password(driver, phone, password):
    """ТС-002: Проверка входа с валидным телефоном, но неверным паролем"""
    assert phone, "PHONE не задан в .env"
    assert password, "Пароль для теста не задан"

    page = LoginPage(driver)
    page.open()

    # Убеждаемся, что страница открылась
    WebDriverWait(driver, 5).until(EC.url_contains("lk.rt.ru"))

    page.click_password_login()
    page.enter_phone(phone)
    page.enter_password(password)
    page.click_login()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")

    # Возможные локаторы для ошибок
    possible_error_locators = [
        (By.CLASS_NAME, "rt-input-container__meta--error"),
        (By.CSS_SELECTOR, ".rt-form-error__text"),
        (By.CSS_SELECTOR, ".form-error-error"),
        (By.ID, "form-error-message"),
        (By.CLASS_NAME, "card-error__message"),
    ]

    wait = WebDriverWait(driver, 5)
    error_text = None

    for locator in possible_error_locators:
        try:
            error_element = wait.until(EC.visibility_of_element_located(locator))
            error_text = error_element.text.strip()
            if error_text:
                break
        except Exception:
            continue

    # Проверяем, что ошибка отображается
    assert error_text, "Ошибка входа не показана!"

    # Проверяем, что в тексте ошибки есть ожидаемые ключевые слова
    expected_keywords = ["неверный", "пароль", "введен", "капча", "ошибка"]
    assert any(keyword in error_text.lower() for keyword in expected_keywords), \
        f"Неожиданное сообщение ошибки: {error_text}"
