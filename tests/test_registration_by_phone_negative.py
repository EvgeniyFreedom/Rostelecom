import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

EXISTING_PHONE = os.getenv("Phone")


@pytest.mark.registration
def test_registration_by_phone_negative(driver):
    """ТС-016: Попытка регистрации с уже существующим телефоном"""

    # Проверяем наличие тестовых данных
    assert EXISTING_PHONE, "PHONE не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Открываем форму авторизации по паролю
    page.click_password_login()

    # Кликаем "Зарегистрироваться"
    page.click_register()

    # Заполняем форму регистрации с уже существующим телефоном
    page.fill_registration_form_phone(
        first_name="Тест",
        last_name="Пользователь",
        phone=EXISTING_PHONE,
        password="Test1234!",
        region="Москва"
    )

    # Сабмитим форму
    page.click_submit_registration()

    # Проверяем появление ошибки
    error_displayed = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((
            By.XPATH,
            "//h2[@class='card-modal__title' and contains(text(),'Учётная запись уже существует')]"
        ))
    )

    assert error_displayed, "Ошибка о существующем пользователе не отображается"
