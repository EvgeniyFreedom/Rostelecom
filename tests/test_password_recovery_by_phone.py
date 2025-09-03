import pytest
import os
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PHONE = os.getenv("PHONE")


@pytest.mark.parametrize("phone", [PHONE])
def test_password_recovery_by_phone(driver, phone):
    """ТС-009: Восстановление пароля по телефону"""

    # Проверяем наличие телефона в .env
    assert phone is not None, "PHONE не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузку правильного URL
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Переходим на форму восстановления пароля
    page.click_password_login()
    page.click_forgot_password()

    # Вводим телефон
    page.enter_phone(phone)
    page.click_continue_recovery()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")