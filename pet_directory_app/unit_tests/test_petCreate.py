import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
import os
from dotenv import load_dotenv
load_dotenv()

class PetCreate_ATS(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 5)

    def test_pet_create_superuser(self):
        user = os.getenv("TEST_SUPERUSER_USERNAME") # must be superuser
        pwd = os.getenv("TEST_SUPERUSER_PASSWORD")

        driver = self.driver
        driver.maximize_window()

        # Login first
        driver.get("http://127.0.0.1:8000/accounts/login/")
        driver.find_element(By.ID, "id_username").send_keys(user)
        driver.find_element(By.ID, "id_password").send_keys(pwd + Keys.RETURN)
        time.sleep(2)

        # Navigate to pet create page
        driver.get("http://127.0.0.1:8000/pets/add/")
        time.sleep(1)

        # Fill out the pet form
        driver.find_element(By.ID, "id_name").send_keys("TestPet")
        species_dropdown = Select(driver.find_element(By.ID, "id_species"))
        species_dropdown.select_by_visible_text("Cat")
        shelter_dropdown = Select(driver.find_element(By.ID, "id_shelter"))
        shelter_dropdown.select_by_visible_text("test")
        driver.find_element(By.ID, "id_age").send_keys("48")
        driver.find_element(By.ID, "id_breed").send_keys("TestBreed")
        driver.find_element(By.ID, "id_color").send_keys("Brown")
        driver.find_element(By.ID, "id_size").send_keys("2 feet")
        driver.find_element(By.ID, "id_description").send_keys("Test description")

        # Submit form
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and normalize-space()='Save']")
        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        submit_button.click()
        time.sleep(2)

        # Verify redirect to pet list page
        try:
            success = driver.find_elements(By.XPATH, "//*[contains(text(), 'TestPet')]")
            if success:
                assert True
            else:
                raise NoSuchElementException
        except NoSuchElementException:
            self.fail("Pet creation failed — TestPet not found on resulting page.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(warnings='ignore')
