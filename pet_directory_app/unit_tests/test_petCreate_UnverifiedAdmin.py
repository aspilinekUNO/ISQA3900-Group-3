import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select

class PetCreate_UnverifiedAdmin_Flow_ATS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)

    def test_unverified_admin_flow_blocked(self):
        driver = self.driver
        driver.maximize_window()

        # create an admin account for existing shelter
        driver.get("http://127.0.0.1:8000/register/")
        time.sleep(1)

        username = "UnverifiedAdmin"
        password = "Test1234!"
        email = "example@mail.com"

        driver.find_element(By.ID, "id_username").send_keys(username)
        driver.find_element(By.ID, "id_email").send_keys(email)
        driver.find_element(By.ID, "id_password1").send_keys(password)
        driver.find_element(By.ID, "id_password2").send_keys(password)

        admin_checkbox = driver.find_element(By.ID, "id_become_shelter_admin")
        admin_checkbox.click()
        time.sleep(0.5)

        shelter_dropdown = Select(driver.find_element(By.ID, "id_existing_shelter"))
        shelter_dropdown.select_by_index(1)  # pick any existing shelter

        # Submit registration
        driver.find_element(By.XPATH, "//button[@type='submit' and normalize-space()='Register']").click()
        time.sleep(2)

        # log in
        driver.get("http://127.0.0.1:8000/accounts/login/")
        time.sleep(1)

        driver.find_element(By.ID, "id_username").send_keys(username)
        driver.find_element(By.ID, "id_password").send_keys(password + Keys.RETURN)
        time.sleep(2)

        # attempt to get to add pet page
        driver.get("http://127.0.0.1:8000/pets/add/")
        time.sleep(2)

        # assert it is blocked (make sure they don't see save btn)
        save_button = driver.find_elements(
            By.XPATH, "//button[@type='submit' and normalize-space()='Save']"
        )

        if save_button:
            self.fail("Unverified admin incorrectly allowed to access pet create page.")
        else:
            assert True

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(warnings='ignore')
