from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginModule:
    def __init__(self, base_url, email, otp_function):
        self.base_url = base_url
        self.email = email
        self.otp_function = otp_function
        self.driver = webdriver.Chrome()

    def login(self):
        try:
            print("Opening the login page...")
            self.driver.get(self.base_url)
            wait = WebDriverWait(self.driver, 15)

            # Step 1: Enter Email
            print("Entering email...")
            email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_input.send_keys(self.email)

            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Next')]")))
            print("Clicking Next...")
            next_button.click()

            # Step 2: Wait for OTP page and interact with OTP input field
            print("Waiting for OTP input field...")
            otp_input = wait.until(EC.presence_of_element_located((By.NAME, "pin")))
            otp = self.otp_function()
            print(f"Entering OTP: {otp}")
            otp_input.send_keys(otp)

            # Re-find the "Go" button in case it got replaced
            go_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[style='width:100px']")))
            print("Clicking Go...")
            go_button.click()

            # Step 3: Verify successful login
            print("Verifying login success...")
            wait.until(EC.url_contains("dashboard"))  # Adjust based on successful login URL
            print("Login successful!")
            return self.driver

        except Exception as e:
            print(f"An error occurred during login: {e}")
            raise

    def close(self):
        print("Closing the browser...")
        self.driver.quit()
