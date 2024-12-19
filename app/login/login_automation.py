from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.common.exceptions import WebDriverException

class LoginModule:
    def __init__(self, base_url, email, otp_function):
        self.base_url = base_url
        self.email = email
        self.otp_function = otp_function
        
        try:
            self.driver = webdriver.Chrome()
            self.wait = WebDriverWait(self.driver, 20)
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
            self.logger = logging.getLogger(__name__)
        except WebDriverException as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise
        
    def open_page(self):
        try:
            self.logger.info("Opening the login page...")
            self.driver.maximize_window()
            self.driver.get(self.base_url)
        except Exception as e:
            self.logger.error(f"Failed to open the page: {e}")
            raise

    def enter_email(self):
        try:
            self.logger.info("Entering email address...")
            email_input = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_input.clear()
            email_input.send_keys(self.email)

            next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]")))
            self.logger.info("Clicking Next button...")
            next_button.click()
        except Exception as e:
            self.logger.error(f"Failed to enter email: {e}")
            raise
        
    def enter_otp(self):
        try:
            self.logger.info("Waiting for OTP input field...")
            otp_input = self.wait.until(EC.presence_of_element_located((By.NAME, "pin")))

            otp = self.otp_function()
            if not otp or not otp.isdigit():
                self.logger.error(f"Invalid OTP provided: {otp}")
                raise ValueError("Invalid OTP")

            self.logger.info(f"Entering OTP: {otp}")
            otp_input.send_keys(otp)

            go_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[style='width:100px']")))
            self.logger.info("Clicking Go button...")
            go_button.click()
        except Exception as e:
            self.logger.error(f"Failed to enter OTP: {e}")
            raise
        
    def login(self):
        try:
            self.open_page()
            self.enter_email()
            self.enter_otp()
            self.logger.info("Login successful!")
            return self.driver
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False
        
    def close(self):
        self.logger.info("Closing the browser...")
        self.driver.quit()