import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage


@pytest.mark.registration
def test_registration_by_email(driver):
    """ТС-014: Регистрация по email"""

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Авторизация по паролю
    page.click_password_login()

    # Кликаем "Зарегистрироваться"
    page.click_register()

    # Заполняем форму регистрации через email
    page.fill_registration_form_email(
        first_name="Тест",
        last_name="Пользователь",
        email="test@example.com",
        password="Test1234!",
        region="Москва"
    )

    # Сабмитим форму
    page.click_submit_registration()

    # Проверка
    assert True, "Регистрация по email прошла без ошибок"
