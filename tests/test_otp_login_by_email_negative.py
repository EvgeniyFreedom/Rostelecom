import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage


@pytest.mark.otp
def test_otp_login_by_email_negative(driver):
    """TC-020: Негативный сценарий входа по временному коду (email)"""

    INVALID_EMAIL = "invalid_email"

    page = LoginPage(driver)
    page.open()

    # Ждём появления формы OTP
    page.wait_for_otp_form()

    # Вводим заведомо невалидный e-mail и жмём "Получить код"
    page.otp_enter_address(INVALID_EMAIL)
    page.otp_click_get_code()

    # Ждём появления сообщения об ошибке
    error_message_el = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "rt-input-container__meta"))
    )
    error_message = error_message_el.text.strip()

    assert error_message, "Ожидалось сообщение об ошибке, но его нет"
    assert "e-mail" in error_message.lower() or "email" in error_message.lower() or "формат" in error_message.lower(), \
        f"Некорректный текст ошибки: {error_message}"

    # Проверяем, что форма ввода кода НЕ появилась
    assert not page.is_recovery_code_input_visible(), \
        "Форма ввода кода не должна появляться для невалидного e-mail"
