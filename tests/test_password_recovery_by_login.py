import pytest
import os
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LOGIN = os.getenv("LOGIN")


@pytest.mark.parametrize("login", [LOGIN])
def test_password_recovery_by_login(driver, login):
    """ТС-012: Восстановление пароля по логину"""

    # Проверяем, что login задан в .env
    assert login is not None, "LOGIN не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Переход к форме восстановления пароля
    page.click_password_login()
    page.click_forgot_password()

    # Переключаемся на вкладку "Логин"
    page.select_login_tab()

    # Вводим логин
    page.enter_login(login)
    page.click_continue_recovery()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")