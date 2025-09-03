import pytest
import os
from pages.login_page import LoginPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

LS = os.getenv("LS")  # Лицевой счёт берём из .env


@pytest.mark.parametrize("ls", [LS])
def test_password_recovery_by_ls(driver, ls):
    """ТС-013: Восстановление пароля по лицевому счёту"""

    # Проверяем, что LS задан в .env
    assert ls is not None, "LS не задан в .env"

    page = LoginPage(driver)
    page.open()

    # Ждём загрузки страницы
    WebDriverWait(driver, 10).until(EC.url_contains("lk.rt.ru"))

    # Открываем форму входа по паролю
    page.click_password_login()

    # Кликаем "Забыл пароль"
    page.click_forgot_password()

    # Переключаемся на вкладку "Лицевой счёт"
    page.select_ls_tab()

    # Вводим номер лицевого счёта
    page.enter_ls(ls)

    # Нажимаем кнопку "Продолжить"
    page.click_continue_recovery()

    # Проверка: появилось ли поле подтверждения следующего шага
    assert page.is_recovery_step_displayed(), "Форма восстановления по ЛС не отобразилась"

    # Если появилась капча — пропускаем тест
    if page.is_captcha_present():
        pytest.skip("Пропускаем тест из-за капчи")