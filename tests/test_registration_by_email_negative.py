import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage

EXISTING_EMAIL = os.getenv("Email")


@pytest.mark.registration
def test_registration_by_email_negative(driver):
    """ТС-015: Попытка регистрации с уже существующим email"""

    # Проверяем наличие тестовых данных
    assert EXISTING_EMAIL, "EMAIL не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Открываем форму авторизации по паролю
    page.click_password_login()

    # Кликаем "Зарегистрироваться"
    page.click_register()

    # Заполняем форму регистрации с уже существующим email
    page.fill_registration_form_email(
        first_name="Тест",
        last_name="Пользователь",
        email=EXISTING_EMAIL,
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
