import os
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.login_page import LoginPage

PHONE = os.getenv("Phone")


@pytest.mark.otp
def test_otp_login_by_phone(driver):
    """TC-017: Вход по временному коду через телефон"""

    # Проверяем наличие тестовых данных
    assert PHONE, "Phone не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Убеждаемся, что форма OTP уже видна
    page.wait_for_otp_form()

    # Вводим телефон и запрашиваем код
    page.otp_enter_address(PHONE)
    page.otp_click_get_code()

    # Проверяем результат
    try:
        page.wait_for_code_form(timeout=10)
        assert True, "Форма подтверждения телефона отображается"
    except TimeoutException:
        if page.is_captcha_present():
            pytest.skip("Пропускаем тест из-за капчи")
        else:
            raise AssertionError("Форма кода не отображается и капча не найдена")
