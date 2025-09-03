import pytest
import os
from dotenv import load_dotenv
from pages.login_page import LoginPage

# Загружаем переменные окружения из .env
load_dotenv()

PHONE = os.getenv("PHONE")
PASSWORD = os.getenv("PASSWORD")


@pytest.mark.parametrize("phone,password", [(PHONE, PASSWORD)])
def test_login_by_valid_phone(driver, phone, password):
    """TC-001: Авторизация по телефону с валидными данными"""

    # Проверяем, что тестовые данные подгрузились
    assert phone, "Переменная PHONE не задана в .env"
    assert password, "Переменная PASSWORD не задана в .env"

    # Открываем страницу авторизации
    page = LoginPage(driver)
    page.open()

    # Выбираем вход по номеру телефона + пароль
    page.click_password_login()

    # Вводим телефон и пароль
    page.enter_phone(phone)
    page.enter_password(password)

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")

    # Нажимаем кнопку «Войти»
    page.click_login()

    # Проверяем, что авторизация прошла успешно
    user_id = page.get_user_id_text()
    assert user_id.isdigit(), f"Ожидался числовой user_id, получили: {user_id}"
