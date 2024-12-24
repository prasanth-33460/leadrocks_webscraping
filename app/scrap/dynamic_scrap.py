import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import json
from pymongo import MongoClient

logging.basicConfig(filename='app/output/scrap.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
class Scrapper:
    def __init__(self, driver,output_file="app/output/file.json"):
        self.driver = driver
        self.browser = driver
        self.output_file = output_file
        self.data_list=[]
        self.wait = WebDriverWait(self.browser, 20)
        
        self.client = MongoClient('mongodb://172.30.100.76:27017')
        self.db = self.client["webscraping_db"]
        self.collection = self.db["scraped_data"]

    def random_sleep(self, min_seconds=1, max_seconds=5):
        sleep_time = random.uniform(min_seconds, max_seconds)  
        time.sleep(sleep_time)
        logger.info(f"Slept for {sleep_time:.2f} seconds")
        
    def save_to_json(self):
        try:
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            with open(self.output_file, 'w') as json_file:
                json.dump(self.data_list, json_file, indent=4)
            logger.info(f"Data successfully saved to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving data to JSON: {e}")
            
    def save_to_mongo(self):
        try:
            for data in self.data_list:
                if '_id' in data:
                    del data['_id']
                    
                self.collection.insert_one(data)
                logger.info(f"Data successfully saved to MongoDB.")
            else:
                logger.warning("No data to insert into MongoDB.")
        except Exception as e:
            logger.error(f"Error saving data to MongoDB: {e}")

    def fill_input_field(self, name, value):
        for attempt in range(5): 
            try:
                input_field = self.wait.until(EC.presence_of_element_located((By.NAME, name)))
                self.wait.until(EC.element_to_be_clickable((By.NAME, name)))
                
                input_field.clear()
                input_field.send_keys(value)
                self.random_sleep()
                
                input_field.send_keys(Keys.ENTER)
                self.random_sleep()
                
                refreshed_field = self.wait.until(EC.presence_of_element_located((By.NAME, name)))
            
                if refreshed_field.get_attribute("value") == value:
                    logger.info(f"Successfully filled '{name}' with '{value}'.")
                    return
                else:
                    logger.warning(f"Verification failed for '{name}'. Retrying...")
            except StaleElementReferenceException:
                logger.warning(f"Stale element reference detected on attempt {attempt + 1}. Retrying...")
                self.random_sleep()
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}: Retrying input for '{name}' due to: {e}")
                self.random_sleep()

        raise Exception(f"Failed to fill input field '{name}' with value '{value}' after 3 attempts.")

    def select_from_dropdown(self, input_name, option_value):
        for attempt in range(3): 
            try:
                input_field = self.wait.until(EC.presence_of_element_located((By.NAME, input_name)))
                input_field.click()
                self.random_sleep()
                
                datalist_id = input_field.get_attribute("list")
                if not datalist_id:
                    raise ValueError(f"No datalist associated with input field '{input_name}'.")
                
                options = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, f'//datalist[@id="{datalist_id}"]/option')))
                
                matched = False
                for option in options:
                    if option.get_attribute("value").strip().lower() == option_value.strip().lower():
                        self.browser.execute_script("arguments[0].value = arguments[1];", input_field, option_value)
                        self.random_sleep()
                        matched = True
                        break
                if matched:
                    logger.info(f"Selected '{option_value}' for field '{input_name}'.")
                    return
                else:
                    raise ValueError(f"Option '{option_value}' not found in the dropdown.")
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed for {input_name} due to: {e}")
                self.random_sleep()

        raise Exception(f"Failed to select '{option_value}' for field '{input_name}' after 3 attempts.")

    def scrape_data(self, global_index):
        try:
            while True:
                results = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="profiles"]//table//tr[@data-id]')))
                for result in results:
                    try:
                        data = self.extract_data_from_result(result, global_index)
                        self.random_sleep()
                        self.data_list.append(data)
                        logger.info(f"Scraped data: {data}")
                        global_index += 1
                        self.save_to_mongo()
                    except Exception as e:
                        logger.warning(f"Error extracting data for a result: {e}")
                
                if not self.go_to_next_page():
                    break
                
            logger.info(f"Data collected: {len(self.data_list)} items.")
            self.save_to_json()
            return global_index
        except Exception as e:
            logger.error(f"Error occurred during scraping: {e}")
            return global_index
        
    def extract_data_from_result(self, result, global_index):
        name = job_title = email = company = company_info = website_link = "N/A"
        try:
            name_element = WebDriverWait(result, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h3')))
            name = name_element.text.strip() or "N/A"
        except Exception as e:
            logger.error(f"Error extracting name for result {global_index}: {e}")
            
        try:
            job_title_element = WebDriverWait(result, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'small')))
            job_title = job_title_element.text.strip() or "N/A"
        except Exception as e:
            logger.error(f"Error extracting job title for result {global_index}: {e}")
            
        try:
            email_element = WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, './/span[contains(@class, "label_work")]')))
            email = email_element.text.strip() or "N/A"  
        except Exception as e:
            logger.error(f"Error occurred while processing result {global_index}: {e}")
            
        self.random_sleep()
        
        try:
            company_element = WebDriverWait(result, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h4')))
            company = company_element.text.strip() or "N/A"
        except Exception as e:
            logger.error(f"Error occurred while processing result {global_index}: {e}")             

        try:
            company_details_element = WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'profiles')]//table//tbody//tr//td[position()=5]")))
            company_info = company_details_element.text.strip() or "N/A"
            company_info = company_info.replace('\n', ', ')
        except Exception as e:
            logger.error(f"Error occurred while processing result {global_index}: {e}")

        try:
            website_element = WebDriverWait(result, 10).until(EC.presence_of_element_located((By.XPATH, './/a[contains(@class, "url")]')))
            website_link = website_element.get_attribute('href').strip() if website_element else "N/A"
        except NoSuchElementException:
            logger.error(f"Error extracting website link for result {global_index}")
        except Exception as e:
            logger.error(f"Unexpected error extracting website link for result {global_index}: {e}")

        return{
            'Result Index': global_index,
            'Name': name,
            'Job Title': job_title,
            'Email': email,
            'Company': company,
            'Company Info': company_info,
            'Website Link': website_link
        }
        
    def go_to_next_page(self):
        try:
            next_page_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "&p=") and contains(text(), ">")]')))
            current_url = self.browser.current_url
            self.random_sleep()
            next_page_button.click()
            
            self.wait.until(lambda driver: driver.current_url != current_url)
            
            self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="profiles"]//table//tr[@data-id]')))
            
            logger.info("Navigated to next page.")
            return True
        except Exception as e:
            logger.warning(f"No more pages or an error occurred: {e}")
            return False