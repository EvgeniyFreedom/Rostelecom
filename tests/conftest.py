import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

load_dotenv()  # загрузить переменные окружения из .env

@pytest.fixture(scope="session")
def rt_phone():
    phone = os.getenv("PHONE")
    assert phone, "Переменная окружения PHONE не задана в .env"
    return phone

@pytest.fixture(scope="session")
def rt_password():
    password = os.getenv("PASSWORD")
    assert password, "Переменная окружения PASSWORD не задана в .env"
    return password

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    service = ChromeService()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
