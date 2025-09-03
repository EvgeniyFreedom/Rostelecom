import pytest
import os
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = os.getenv("EMAIL")


@pytest.mark.parametrize("email", [EMAIL])
def test_password_recovery_by_email(driver, email):
    """ТС-010: Восстановление пароля по email"""

    # Проверяем, что email задан в .env
    assert email is not None, "EMAIL не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Переход к форме восстановления пароля
    page.click_password_login()
    page.click_forgot_password()

    # Переключаемся на вкладку Email
    page.select_email_tab()

    # Вводим email
    page.enter_email(email)
    page.click_continue_recovery()

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")