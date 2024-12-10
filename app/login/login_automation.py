from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginAutomation:
    def login_to_leadrocks(email):
        driver = webdriver.Chrome()  
        driver.maximize_window()

        try:
            driver.get("https://leadrocks.io/auth")

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
            email_input = driver.find_element(By.NAME, "email")
            email_input.send_keys(email)

            next_button = driver.find_element(By.XPATH, "//button[text()='Next']")
            next_button.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "pin")))

            print("A 5-digit PIN has been sent to your email. Please enter it manually.")
            input("Press Enter after entering the PIN and reaching the homepage...")
            print("Login successful!")
            return driver

        except Exception as e:
            print(f"An error occurred: {e}")
            
        finally:
            driver.quit()