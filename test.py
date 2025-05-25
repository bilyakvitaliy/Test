from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest
import os

# Page Object Model
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.TAG_NAME, "button")
        self.error_msg = (By.ID, "errorMsg")

    def load(self, path):
        self.driver.get("file://" + os.path.abspath(path))

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def is_error_displayed(self):
        return self.driver.find_element(*self.error_msg).is_displayed()

# Фікстура для запуску WebDriver
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# Тест з неправильними даними
def test_login_fail(driver):
    page = LoginPage(driver)
    page.load("index.html")  # файл повинен бути поруч
    page.login("wrong", "wrong")
    assert page.is_error_displayed(), "Error message should be visible!"
