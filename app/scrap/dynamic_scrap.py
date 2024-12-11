from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# # Setup Chrome driver options

# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")

# Set the path for ChromeDriver
# service = Service('/path/to/chromedriver')  # Update with your chromedriver path

# Initialize the WebDriver
browser = webdriver.Chrome()

try:
    # Open the login page
    url = "https://leadrocks.io/my"
    browser.get(url)
    
    # Wait until the email input is present
    email_input = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.NAME, 'email')))
    email_input.clear()
    email_input.send_keys('prasanth33460@gmail.com')  # Replace with the email you want to use
    
    # Click the "Next" button
    next_button = WebDriverWait(browser, 30).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]')))
    next_button.click()
    
    # Wait until the "Go" button is present
    go_button = WebDriverWait(browser, 120).until(EC.element_to_be_clickable((By.XPATH, '//button/div[text()="Go"]')))
    go_button.click()
    
    # Wait for the homepage to fully load
    WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.NAME, 'position')))
    
    # Function to fill fields with retry logic
    def fill_input_field(name, value):
        """Locate and fill input field, handling stale element reference errors."""
        for _ in range(3):  # Retry up to 3 times
            try:
                input_field = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, name)))
                input_field.clear()
                input_field.send_keys(value)
                time.sleep(1)
                input_field.send_keys(Keys.ENTER)
                break  # Exit loop if successful
            except Exception as e:
                print(f"Retrying input for {name} due to error: {e}")
    
    # Step 3: Fill out the search form
    fill_input_field('position', 'Software Engineer')
    fill_input_field('company', 'Google')
    fill_input_field('geo', 'United States')
    fill_input_field('industry', 'information technology and services')  # Must match option exactly
    fill_input_field('team_size', '10001+')
    # fill_input_field('revenue_range', '$1M to $10M')
    # fill_input_field('total_funding', '$10M to $100M')
    # # fill_field('industry', 'Information Technology')
    # fill_field('team_size', '11-50')
    # fill_field('revenue_range', '$1M to $10M')
    # fill_field('total_funding', '$10M to $100M')
    
    def select_from_dropdown(field_xpath, option_text):
        """Selects an option from a custom dropdown by clicking it and selecting the option."""
        try:
            # Click the dropdown to reveal options
            dropdown = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, field_xpath)))
            dropdown.click()
            
            # Wait for and click the option from the dropdown
            option_xpath = f'//li[contains(text(), "{option_text}")]'
            option = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, option_xpath)))
            option.click()
            
            print(f"Selected '{option_text}' from the dropdown.")
            
        except Exception as e:
            print(f"Failed to select '{option_text}' from the dropdown: {e}")
            
            
    select_from_dropdown('//input[@name="industry"]/following-sibling::div', 'information technology and services')
    select_from_dropdown('//input[@name="team_size"]/following-sibling::div', '10001+')
    # select_from_dropdown('//input[@name="revenue_range"]/following-sibling::div', '$1M to $10M')
    # select_from_dropdown('//input[@name="total_funding"]/following-sibling::div', '$10M to $100M')
    
    # Click the "Search" button
    search_button = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Search"]')))
    search_button.click()
    
    # Wait for the search results to load
    WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="profiles"]//table//tr[@data-id]')))
    
    # Extract and print the search results (example, this part depends on the page's structure)
    results = browser.find_elements(By.XPATH, '//div[@class="profiles"]//table//tr[@data-id]')
    for index, result in enumerate(results):
        try:
            name = result.find_element(By.TAG_NAME, 'h3').text
            job_title = result.find_element(By.TAG_NAME, 'small').text
            email = result.find_element(By.XPATH, './/span[contains(@class, "label_work")]').text
            company = result.find_element(By.TAG_NAME, 'h4').text
            company_details = result.find_elements(By.TAG_NAME, 'small')
            company_info = ", ".join([detail.text for detail in company_details])
            website_link = result.find_element(By.XPATH, './/a[contains(@class, "url")]').get_attribute('href')
            
            print(f"Result {index + 1}:")
            print(f"  Name: {name}")
            print(f"  Job Title: {job_title}")
            print(f"  Email: {email}")
            print(f"  Company: {company}")
            print(f"  Company Info: {company_info}")
            print(f"  Website: {website_link}")
            print("------------------------")
        except Exception as e:
            print(f"An error occurred while processing result {index + 1}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    browser.quit()
