from app.scrap.dynamic_scrap import Scrapper
from app.login.login_automation import LoginModule
from fastapi import FastAPI, HTTPException
import os
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

app = FastAPI()

def get_otp():
    return input("Enter the OTP: ")

@app.get("/")
def scrape_data():
    log_file_path = os.path.abspath("app/output/main.log")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    base_url = "https://leadrocks.io/my"
    email = "prasanth33460@gmail.com"
    output_file_path = os.path.abspath("app/output/output_file.json")
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    
    try:
        login_module = LoginModule(base_url, email, get_otp)
        driver = login_module.login()
        if not driver:
            logger.error("Login failed. Exiting program.")
            raise HTTPException(status_code=400, detail="Login failed")
        logger.info("Login successful. Initializing scraper...")
        
        scraper = Scrapper(driver, output_file=output_file_path)
        logger.info("Filling input fields before starting the scraping...")
        
        scraper.fill_input_field('position', 'Software Engineer') 
        scraper.fill_input_field('company', 'Google') 
        scraper.fill_input_field('geo', 'United States')
        
        scraper.select_from_dropdown('industry', 'Information Technology and Services')
        scraper.select_from_dropdown('team_size', '10001+')
        # scraper.select_from_dropdown('revenue_range', '$1M to $10M')
        # scraper.select_from_dropdown('total_funding', '$10M to $100M')
        
        search_button = WebDriverWait(scraper.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Search"]')))
        search_button.click()
        
        WebDriverWait(scraper.browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="profiles"]//table//tr[@data-id]')))
        logger.info("Input fields filled and search initiated. Starting dynamic scraping...")
        
        global_index = 1
        while True:
            global_index = scraper.scrape_data(global_index)
            if global_index == -1: 
                logger.info("No new data found or end of pages reached.")
                break
            scraper.random_sleep() 
        
        logger.info("Scraping completed successfully.")
        scraper.save_to_json()
        logger.info("Data saved to JSON file...")
        return {"status": "success", "message": "Scraping completed successfully.", "output_file": output_file_path}
            
    except Exception as e:
        logger.error(f"An error occurred during execution: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
        
    finally:
        if driver:
            driver.quit()
            logger.info("Browser closed.")
        login_module.close()