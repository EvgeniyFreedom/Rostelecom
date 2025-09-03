import pytest
import os
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

# Загружаем переменные окружения
load_dotenv()

EMAIL = os.getenv("EMAIL")
INVALID_PASSWORD = "wrong_password123"


@pytest.mark.parametrize("email,password", [
    (EMAIL, INVALID_PASSWORD),
])
def test_login_by_email_invalid_password(driver, email, password):
    """ТС-004: Негативный тест: вход по email с неверным паролем"""
    assert email, "EMAIL не задан в .env"
    assert password, "Пароль для теста не задан"

    page = LoginPage(driver)
    page.open()

    wait = WebDriverWait(driver, 5)
    wait.until(EC.url_contains("lk.rt.ru"))

    # Переходим в режим входа по паролю
    page.click_password_login()

    # Переключаемся на вкладку "Почта"
    try:
        email_tab = driver.find_element(By.ID, "t-btn-tab-mail")
        email_tab.click()
    except Exception:
        pass  # если вкладка уже активна, пропускаем

    # Вводим данные
    page.enter_email(email)
    page.enter_password(password)
    page.click_login()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")

    # Возможные локаторы сообщения об ошибке
    possible_error_locators = [
        (By.CLASS_NAME, "rt-input-container__meta--error"),
        (By.CSS_SELECTOR, ".rt-form-error__text"),
        (By.CSS_SELECTOR, ".form-error-error"),
        (By.ID, "form-error-message"),
        (By.CLASS_NAME, "card-error__message"),
    ]

    error_text = None
    for locator in possible_error_locators:
        try:
            error_element = wait.until(EC.visibility_of_element_located(locator))
            error_text = error_element.text.strip()
            if error_text:
                break
        except Exception:
            continue

    # Проверки
    assert error_text, "Ошибка входа не показана!"
    expected_keywords = ["неверный", "пароль", "введен текст", "ошибка"]
    assert any(keyword in error_text.lower() for keyword in expected_keywords), \
        f"Неожиданное сообщение ошибки: {error_text}"
