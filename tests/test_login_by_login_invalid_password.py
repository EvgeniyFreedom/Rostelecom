import pytest
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

# Загружаем переменные окружения
load_dotenv()

LOGIN = os.getenv("LOGIN")
INVALID_PASSWORD = "WrongPass123"


@pytest.mark.parametrize("login,password", [
    (LOGIN, INVALID_PASSWORD),
])
def test_login_by_login_invalid_password(driver, login, password):
    """ТС-006: Негативный тест: вход по логину с неверным паролем"""
    assert login, "LOGIN не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки формы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Переход на форму входа по паролю
    page.click_password_login()
    page.select_login_tab()

    # Вводим логин и неверный пароль
    page.enter_login(login)
    page.enter_password(password)
    page.click_login()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")

    # Проверяем сообщение об ошибке
    error_text = page.get_error_text()
    assert error_text, "Сообщение об ошибке не отображается"
    assert "Неверный логин или пароль" in error_text or "Неверно введены логин или пароль" in error_text, \
        f"Неожиданное сообщение об ошибке: {error_text}"
