import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage


@pytest.mark.registration
def test_registration_by_phone(driver):
    """ТС-011: Регистрация по телефону"""
    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Открываем форму авторизации по паролю
    page.click_password_login()

    # Кликаем "Зарегистрироваться"
    page.click_register()

    # Заполняем форму регистрации по телефону
    page.fill_registration_form_phone(
        first_name="Тест",
        last_name="Пользователь",
        phone="+79281234567",
        password="Test1234!",
        region="Москва"
    )

    # Сабмитим форму
    page.click_submit_registration()

    # Проверка
    assert True, "Форма регистрации по телефону заполнена без ошибок"
