import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import os
from dotenv import load_dotenv
load_dotenv()

class Login_ATS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)

    def test_successful_login(self):
        user = os.getenv("TEST_SUPERUSER_USERNAME")
        pwd = os.getenv("TEST_SUPERUSER_PASSWORD")

        driver = self.driver
        driver.maximize_window()

        # Go to login page
        driver.get("http://127.0.0.1:8000/accounts/login/")

        # Enter username
        elem = driver.find_element(By.ID, "id_username")
        elem.send_keys(user)

        # Enter password
        elem = driver.find_element(By.ID, "id_password")
        elem.send_keys(pwd)
        time.sleep(1)
        elem.send_keys(Keys.RETURN)

        # Wait for redirect
        time.sleep(2)

        # Check for logout button
        try:
            logout_button = driver.find_elements(
                By.XPATH, "//button[normalize-space()='Logout']"
            )
            if logout_button:
                assert True
            else:
                raise NoSuchElementException
        except NoSuchElementException:
            self.fail("Login failed — logout button not found.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(warnings='ignore')
