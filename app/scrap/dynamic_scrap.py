from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv 

class Scrapper:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.output_file = 'app/output/scrapped_data.csv'
        self.header_written = False
    
    def write_to_csv(self, data):
        """Writes data to a CSV file with the structure of terminal output."""
        try:
            with open(self.output_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                
                # Write header only once
                if not self.header_written:
                    writer.writerow(['Result Index', 'Name', 'Job Title', 'Email', 'Company', 'Company Info', 'Website Link'])
                    self.header_written = True
                
                # Write data for each result
                writer.writerow([data['Result Index'], data['Name'], data['Job Title'], data['Email'], data['Company'], data['Company Info'], data['Website Link']])
            print("Data successfully written to CSV.")
        except Exception as e:
            print(f"Error writing to CSV: {e}")

    def fill_input_field(self, name, value):
        for _ in range(3):  # Retry up to 3 times
            try:
                input_field = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.NAME, name)))
                input_field.clear()
                input_field.send_keys(value)
                time.sleep(2)  # Added delay to allow for any autocomplete suggestions
                input_field.send_keys(Keys.ARROW_DOWN)
                input_field.send_keys(Keys.ENTER)
                break
            except Exception as e:
                print(f"Retrying input for {name} due to: {e}")

    def select_from_dropdown(self, input_name, option_value):
        """
        Selects an option from an input field with a datalist by simulating user input.

        Parameters:
            input_name (str): The `name` attribute of the input field.
            option_value (str): The value to select from the datalist.
        """
        for _ in range(3):  # Retry up to 3 times
            try:
                # Wait for the input field to be present
                input_field = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.NAME, input_name)))
                
                # Clear any existing input and enter the desired value
                input_field.click()
                time.sleep(2)  # Allow time for the datalist suggestions to populate
                
                datalist_id = input_field.get_attribute("list")
                options = self.browser.find_elements(By.XPATH, f'//datalist[@id="{datalist_id}"]/option')
                
                for option in options:
                    if option.get_attribute("value") == option_value:
                        option.click()  # Select the desired option
                        time.sleep(1)
                        break
                    else:
                        raise ValueError(f"Option '{option_value}' not found in the datalist.")

                print(f"Selected '{option_value}' for field '{input_name}'.")
                return  # Exit loop on success
            
            except Exception as e:
                print(f"Retrying selection for {input_name} due to: {e}")
                time.sleep(2)  # Wait before retry
        raise Exception(f"Failed to select '{option_value}' for field '{input_name}' after 3 attempts.")
                
    def extract_results(self, global_index):
        results = WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="profiles"]//table//tr[@data-id]')))
        for result in results:
            try:
                name = result.find_element(By.TAG_NAME, 'h3').text
                job_title = result.find_element(By.TAG_NAME, 'small').text
                
                try:
                    email = result.find_element(By.XPATH, './/span[contains(@class, "label_work")]').text
                except Exception as e:
                    email = "N/A"  # If element not found, assign "N/A"
                    print(f"Error occurred while processing result {global_index}: {e}")
                
                
                try:
                    company = result.find_element(By.TAG_NAME, 'h4').text
                except:
                    company = "N/A"
                    print(f"Error occurred while processing result {global_index}: {e}")                
                
                
                try:
                    company_details = result.find_elements(By.TAG_NAME, 'small')
                except:
                    company_details = "N/A"
                    print(f"Error occurred while processing result {global_index}: {e}")

                    
                try:
                    company_info = ", ".join([detail.text for detail in company_details])
                except:
                    company_info = "N/A"
                    print(f"Error occurred while processing result {global_index}: {e}")

                
                try:
                    website_link = result.find_element(By.XPATH, './/a[contains(@class, "url")]').get_attribute('href')
                except:
                    website_link = "N/A"  # If website link is missing, set to "N/A"
                    print(f"Error occurred while processing result {global_index}: {e}")

                # print(f"Result {global_index}:")
                # print(f"  Name: {name}")
                # print(f"  Job Title: {job_title}")
                # print(f"  Email: {email}")
                # print(f"  Company: {company}")
                # print(f"  Company Info: {company_info}")
                # print(f"  Website: {website_link}")
                # print("------------------------")
                
                data = {
                    'Result Index': global_index,
                    'Name': name,
                    'Job Title': job_title,
                    'Email': email,
                    'Company': company,
                    'Company Info': company_info,
                    'Website Link': website_link
                }
                self.write_to_csv(data)
                global_index += 1
            
            except Exception as e:
                print(f"An error occurred while processing result {global_index}: {e}")
            
        return global_index

if __name__ == "__main__":
    scrap = Scrapper()
    try:
        # Open the login page
        url = "https://leadrocks.io/my"
        scrap.browser.get(url)
        
        # Wait for the email input to be present
        email_input = WebDriverWait(scrap.browser, 20).until(EC.presence_of_element_located((By.NAME, 'email')))
        email_input.clear()
        email_input.send_keys('prasanth33460@gmail.com')  # Replace with the email you want to use
        
        # Click the "Next" button
        next_button = WebDriverWait(scrap.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]')))
        next_button.click()
        
        # Wait until the "Go" button is present
        go_button = WebDriverWait(scrap.browser, 60).until(EC.element_to_be_clickable((By.XPATH, '//button/div[text()="Go"]')))
        go_button.click()
        
        # Wait for the homepage to load
        WebDriverWait(scrap.browser, 20).until(EC.presence_of_element_located((By.NAME, 'position')))
        
        # Manually enter job title and company name/URL
        scrap.fill_input_field('position', 'Software Engineer')  # Manually enter the job title
        scrap.fill_input_field('company', 'Google')  # Manually enter the company name or URL
        scrap.fill_input_field('geo', 'United States')
        
        # Use drop-down selection for location, industry, team size, revenue range, and total funding
        # scrap.select_from_dropdown('industry', 'information technology and services')
        # scrap.select_from_dropdown('team_size', '10001+')
        # scrap.select_from_dropdown('revenue_range', '$1M to $10M')
        # scrap.select_from_dropdown('total_funding', '$10M to $100M')
        
        # Click the "Search" button
        search_button = WebDriverWait(scrap.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Search"]')))
        search_button.click()
        
        global_index = 1

        while True:
            global_index = scrap.extract_results(global_index)
            
            try:
                # Locate the "next page" button
                next_page_button = WebDriverWait(scrap.browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "&p=") and contains(text(), ">")]'))
                )
                
                # Save the current URL to check for changes
                current_url = scrap.browser.current_url
                
                # Click the "next page" button
                next_page_button.click()
                
                # Wait for the URL to change
                WebDriverWait(scrap.browser, 20).until(lambda driver: driver.current_url != current_url)
                
                # Wait for the next page's results to load
                WebDriverWait(scrap.browser, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="profiles"]//table//tr[@data-id]'))
                )
                
                # Add a delay to mimic human behavior
                time.sleep(10)
                
            except Exception as e:
                print("No more pages or an error occurred: ", e)
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        scrap.browser.quit()
