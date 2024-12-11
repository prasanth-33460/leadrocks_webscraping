import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.login.login_automation import LoginModule


class Scrapper:
    def __init__(self, base_url, email, otp_function):
        self.base_url = base_url
        self.email = email
        self.otp_function = otp_function
        self.login_module = LoginModule(base_url, email, otp_function)
        
    def scrap_homepage(self):
        try:
            print('Logging in..')
            self.login_module.login()
            driver = self.login_module.driver
            wait = WebDriverWait(driver, 30)
            print("Waiting for homepage to load...")
            homepage_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='flex']")))
            print("Homepage Loaded...")
            print("Scraping dynamic elements...")
            dynamic_elements = driver.find_elements(By.XPATH, "//div[@class='flex']//div[@class='line']")
            for index, element in enumerate(dynamic_elements, start=1):
                label = element.find_element(By.XPATH, ".//label").text
                input_value = element.find_element(By.XPATH, ".//input").get_attribute("value")
                print(f"Element {index}: {label} - {input_value}")
            
        except Exception as e:
            print(f'An error occurred during Scrapping:  {e}')
            
        finally:
            self.login_module.driver.quit()
        