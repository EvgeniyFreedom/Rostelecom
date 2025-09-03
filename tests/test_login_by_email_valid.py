import pytest
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

# Загружаем переменные окружения
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


@pytest.mark.parametrize("email,password", [
    (EMAIL, PASSWORD),
])
def test_login_by_email_valid_password(driver, email, password):
    """ТС-003: Проверка входа с валидным email и паролем"""
    assert email, "EMAIL не задан в .env"
    assert password, "PASSWORD не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы авторизации
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Включаем режим входа по логину/паролю
    page.click_password_login()

    # Вводим данные
    page.enter_email(email)
    page.enter_password(password)
    page.click_login()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")

    # Проверяем успешный вход
    user_id = page.get_user_id_text()
    assert user_id and user_id.strip(), "ID пользователя не найден после входа"
