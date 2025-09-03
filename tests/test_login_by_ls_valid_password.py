import pytest
import os
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Загружаем переменные окружения
LS = os.getenv("LS")
PASSWORD = os.getenv("PASSWORD")


@pytest.mark.parametrize("ls_number,password", [
    (LS, PASSWORD),
])
def test_login_by_ls_valid_password(driver, ls_number, password):
    """ТС-007: Позитивный тест: вход по лицевому счёту с валидным паролем"""
    assert ls_number, "LS не задан в .env"
    assert password, "PASSWORD не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём, что загрузился нужный URL
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Переход на форму входа по паролю и выбор вкладки ЛС
    page.click_password_login()
    page.select_ls_tab()

    # Вводим лицевой счёт и пароль
    page.enter_ls(ls_number)
    page.enter_password(password)
    page.click_login()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")

    # Проверяем успешную авторизацию
    assert page.is_logged_in(), "Авторизация по ЛС не удалась"
