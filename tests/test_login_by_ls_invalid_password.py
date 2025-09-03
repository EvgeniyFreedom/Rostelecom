import pytest
import os
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Переменные окружения и невалидный пароль
LS = os.getenv("LS")
INVALID_PASSWORD = "WrongPass123"


@pytest.mark.parametrize("ls_number,password", [
    (LS, INVALID_PASSWORD),
])
def test_login_by_ls_invalid_password(driver, ls_number, password):
    """ТС-008: Негативный тест: вход по лицевому счёту с неверным паролем"""
    assert ls_number, "LS не задан в .env"
    assert password, "Пароль для теста не задан"

    page = LoginPage(driver)
    page.open()

    # Ждём, что загрузился нужный URL
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Переход на форму входа по паролю и выбор вкладки ЛС
    page.click_password_login()
    page.select_ls_tab()

    # Вводим ЛС и неверный пароль
    page.enter_ls(ls_number)
    page.enter_password(password)
    page.click_login()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")

    # Проверяем сообщение об ошибке
    error_text = page.get_error_text()
    assert error_text, "Сообщение об ошибке не отображается"
    assert any(msg in error_text for msg in [
        "Неверный логин или пароль",
        "Неверно введены логин или пароль"
    ]), f"Неожиданное сообщение об ошибке: {error_text}"
