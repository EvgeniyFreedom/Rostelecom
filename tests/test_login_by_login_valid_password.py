import pytest
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

# Загружаем переменные окружения
load_dotenv()

LOGIN = os.getenv("LOGIN")      # логин из .env
PASSWORD = os.getenv("PASSWORD")  # пароль из .env


@pytest.mark.parametrize("login,password", [
    (LOGIN, PASSWORD),
])
def test_login_by_login_valid_password(driver, login, password):
    """ТС-005: Позитивный тест: вход по логину и валидному паролю"""
    assert login, "LOGIN не задан в .env"
    assert password, "PASSWORD не задан в .env"

    page = LoginPage(driver)
    page.open()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("lk.rt.ru"))

    # Переходим на форму входа по паролю
    page.click_password_login()

    # Переключаемся на вкладку "Логин"
    page.select_login_tab()

    # Вводим логин и пароль
    page.enter_login(login)
    page.enter_password(password)
    page.click_login()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")

    # Проверяем, что пользователь вошёл
    user_id = page.get_user_id_text()
    assert user_id and user_id.strip() != "", "ID пользователя не найден после входа"
