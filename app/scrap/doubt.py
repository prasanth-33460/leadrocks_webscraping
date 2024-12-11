from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app.login.login_automation import LoginModule

# Initialize the WebDriver
driver = webdriver.Chrome()  # Adjust path to your ChromeDriver if needed
driver.get("https://leadrocks.io/auth")  # Replace with the actual webpage URL

# Login (if required, import your login logic or use fields directly)
# Assuming you already have a login script/module
# login_automation.login(driver)

# Wait for the page to load
wait = WebDriverWait(driver, 10)

# Fill the "Job title" and "Company name or URL" fields
job_title_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='position']")))
company_name_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='company']")))

job_title_input.send_keys("Software Engineer")  # Replace with the desired job title
company_name_input.send_keys("Amazon")  # Replace with the desired company name

# Click the "Search" button
search_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
search_button.click()

# Wait for search results to load
results_container = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='results-container']")))

# Scrape search results
results = driver.find_elements(By.XPATH, "//div[@class='result-item']")

for result in results:
    job_title = result.find_element(By.XPATH, ".//div[@class='job-title']").text
    company_name = result.find_element(By.XPATH, ".//div[@class='company-name']").text
    email = result.find_element(By.XPATH, ".//div[@class='email']").text

    print(f"Job Title: {job_title}, Company Name: {company_name}, Email: {email}")

# Close the driver
driver.quit()
