from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://lk.rt.ru/"
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        """Открываем страницу входа"""
        self.driver.get(self.url)

    def click_password_login(self):
        """Кнопка 'Войти со своим паролем'. Если уже на форме — тихо продолжаем"""
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.ID, "standard_auth_btn")))
            btn.click()
        except Exception:
            pass

    def enter_phone(self, phone: str):
        """Ввод телефона (поле username)"""
        input_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        input_field.clear()
        input_field.send_keys(phone)

    def enter_email(self, email: str):
        """Ввод email (поле username)"""
        self.enter_phone(email)

    def enter_login(self, login: str):
        """Ввод логина (поле username)"""
        self.enter_phone(login)

    def select_ls_tab(self):
        """Переключает вкладку на 'Лицевой счёт' и дожидается активации"""
        try:
            tab = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "t-btn-tab-ls"))
            )
            tab.click()
            # ждём, что вкладка стала активной, класс или плейсхолдер поменялся
            WebDriverWait(self.driver, 5).until(
                lambda d: 'active' in (tab.get_attribute('class') or '').lower()
                or 'счёт' in (d.find_element(By.ID, 'username').get_attribute('placeholder') or '').lower()
                or 'счет' in (d.find_element(By.ID, 'username').get_attribute('placeholder') or '').lower()
            )
            # подстраховка: фокус и очистка поля
            field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            field.click()
            field.clear()
        except Exception as e:
            raise AssertionError("Не удалось переключиться на вкладку ЛС") from e

    def enter_ls(self, ls_number):
        """Вводит лицевой счёт в соответствующее поле"""
        ls_input = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        ls_input.clear()
        ls_input.send_keys(ls_number)

    def enter_password(self, password: str):
        """Ввод пароля"""
        input_password = self.driver.find_element(By.ID, "password")
        input_password.clear()
        input_password.send_keys(password)

    def click_login(self):
        """Кнопка 'Войти'"""
        login_btn = self.driver.find_element(By.ID, "kc-login")
        login_btn.click()

    def get_user_id_text(self) -> str:
        """Текст ID пользователя после входа"""
        user_block = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "app-header_profile_header_user"))
        )
        return user_block.find_element(By.CLASS_NAME, "color_black").text

    def is_captcha_present(self, timeout: int = 3) -> bool:
        """Проверяет, появилась ли капча на странице, возвращает True, если есть элемент капчи"""
        possible_locators = [
            (By.CLASS_NAME, "rt-captcha"),
            (By.CLASS_NAME, "rt-captcha__image"),
            (By.CSS_SELECTOR, "img.rt-captcha__image"),
        ]
        for by, value in possible_locators:
            try:
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
                return True
            except Exception:
                continue
        return False

    def get_error_text(self) -> str:
        """Универсальное чтение текста ошибки"""
        locators = [
            (By.ID, "form-error-message"),
            (By.CLASS_NAME, "card-error__message"),
            (By.CLASS_NAME, "rt-input-container__meta--error"),
            (By.CSS_SELECTOR, ".rt-form-error__text"),
            (By.CSS_SELECTOR, ".form-error-error"),
        ]
        for locator in locators:
            try:
                el = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(locator))
                txt = el.text.strip()
                if txt:
                    return txt
            except Exception:
                continue
        return None

    def select_login_tab(self):
        """Переключает вкладку на 'Логин' и дожидается активации"""
        try:
            tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-login")))
            tab.click()
            # ждём активность вкладки или смену плейсхолдера поля username
            WebDriverWait(self.driver, 5).until(
                lambda d: 'active' in (tab.get_attribute('class') or '').lower()
                or 'логин' in (d.find_element(By.ID, 'username').get_attribute('placeholder') or '').lower()
            )
            # подстраховка: клик по полю, очистка
            field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            field.click()
            field.clear()
        except Exception as e:
            raise AssertionError("Не удалось переключиться на вкладку 'Логин'") from e

    def is_logged_in(self) -> bool:
        """Проверяет, что пользователь авторизован — ищет хотя бы один из элементов профиля"""
        possible_locators = [
            (By.CLASS_NAME, "app-header_profile_header_user"),
            (By.CLASS_NAME, "user-info__name"),
            (By.XPATH, "//span[contains(text(),'Лицевой счет')]"),
            (By.XPATH, "//div[contains(@class,'profile-card')]"),
        ]
        for by, value in possible_locators:
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((by, value))
                )
                return True
            except:
                continue
        return False

    def click_forgot_password(self):
        """Кнопка 'Забыли пароль?'"""
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.ID, "forgot_password")))
            btn.click()
        except Exception:
            pass

    def click_continue_recovery(self):
        """Кнопка 'Продолжить' на форме восстановления"""
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.ID, "continue_recovery")))
            btn.click()
        except Exception:
            pass

    def is_recovery_code_input_visible(self) -> bool:
        """Проверка, что поле ввода кода восстановления отображается"""
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, "recovery_code")))
            return True
        except Exception:
            return False

    def select_email_tab(self):
        """Переключает вкладку на 'Почта' и дожидается активации"""
        try:
            tab = self.wait.until(EC.element_to_be_clickable((By.ID, "t-btn-tab-mail")))
            tab.click()
            WebDriverWait(self.driver, 5).until(
                lambda d: 'active' in (tab.get_attribute('class') or '').lower()
                or 'e-mail' in (d.find_element(By.ID, 'username').get_attribute('placeholder') or '').lower()
                or 'email' in (d.find_element(By.ID, 'username').get_attribute('placeholder') or '').lower()
            )
            field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
            field.click()
            field.clear()
        except Exception as e:
            raise AssertionError("Не удалось переключиться на вкладку 'Почта'") from e

    def click_register(self):
        # ВАЖНО: именно эта кнопка переводит к регистрации
        btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "kc-register"))
        )
        btn.click()

    def wait_registration_form(self):
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "page-right"))
        )

    def fill_registration_form_phone(self, first_name, last_name, phone, password, region):
        wait = WebDriverWait(self.driver, 15)

        first_name_input = wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
        first_name_input.clear()
        first_name_input.send_keys(first_name)

        last_name_input = wait.until(EC.visibility_of_element_located((By.NAME, "lastName")))
        last_name_input.clear()
        last_name_input.send_keys(last_name)

        phone_input = wait.until(EC.visibility_of_element_located((By.ID, "address")))
        phone_input.clear()
        phone_input.send_keys(phone)

        pw = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        pw.clear()
        pw.send_keys(password)

        pw2 = wait.until(EC.visibility_of_element_located((By.ID, "password-confirm")))
        pw2.clear()
        pw2.send_keys(password)

        self.select_region(region)

    def fill_registration_form_email(self, first_name, last_name, email, password, region):
        wait = WebDriverWait(self.driver, 15)

        first_name_input = wait.until(EC.visibility_of_element_located((By.NAME, "firstName")))
        first_name_input.clear()
        first_name_input.send_keys(first_name)

        last_name_input = wait.until(EC.visibility_of_element_located((By.NAME, "lastName")))
        last_name_input.clear()
        last_name_input.send_keys(last_name)

        email_input = wait.until(EC.visibility_of_element_located((By.ID, "address")))
        email_input.clear()
        email_input.send_keys(email)

        pw = wait.until(EC.visibility_of_element_located((By.ID, "password")))
        pw.clear()
        pw.send_keys(password)

        pw2 = wait.until(EC.visibility_of_element_located((By.ID, "password-confirm")))
        pw2.clear()
        pw2.send_keys(password)

        self.select_region(region)

    def select_region(self, region_name="Москва"):
        region_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[contains(@class,'rt-select__input')]"))
        )
        region_input.click()

        dropdown_options = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class,'rt-select__list-item')]"))
        )

        for option in dropdown_options:
            if region_name.lower() in option.text.lower():
                option.click()
                return

        raise Exception(
            f"Регион с текстом '{region_name}' не найден. Доступные варианты: {[opt.text for opt in dropdown_options]}")

    def is_registration_error_displayed(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h2[@class='card-modal__title' and contains(text(),'Учётная запись уже существует')]")
                )
            )
            return True
        except:
            return False

    def is_recovery_step_displayed(self, timeout: int = 10) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((
                    By.XPATH, "//input[@name='code' or contains(@placeholder, 'код')]"
                ))
            )
            return True
        except:
            return False

    def click_submit_registration(self):
        wait = WebDriverWait(self.driver, 10)
        button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        button.click()

    # -------------------- OTP --------------------

    def wait_for_otp_form(self, timeout: int = 15):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located((By.ID, "address")))
        wait.until(EC.element_to_be_clickable((By.ID, "otp_get_code")))
        return True

    def otp_enter_address(self, value: str):
        inp = self.wait.until(EC.visibility_of_element_located((By.ID, "address")))
        inp.clear()
        inp.send_keys(value)

    def otp_click_get_code(self):
        btn = self.wait.until(EC.element_to_be_clickable((By.ID, "otp_get_code")))
        btn.click()

    def wait_for_code_form(self, timeout: int = 15):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(
            lambda d: d.find_elements(By.ID, "rt-code-input")
                      or d.find_elements(By.ID, "otp-code-timeout")
        )

    def get_error_message(self, timeout=5):
        try:
            error = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rt-input-container__meta--error"))
            )
            return error.text
        except Exception:
            return None

    def is_otp_code_input_visible(self, timeout: int = 5) -> bool:
        try:
            element = self.driver.find_element("id", "rt-code-0")
            return element.is_displayed()
        except NoSuchElementException:
            return False
