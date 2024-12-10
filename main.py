from scrap.login_automation import LoginAutomation
login = LoginAutomation()

if __name__ == "__main__":
    user_email = input("Enter your email for Lead Rocks login: ")
    driver = login.login_to_leadrocks(user_email)

    # Add code here to start scraping after successful login
    # e.g., scrape_leadrocks(driver)

    # Close the driver when done
    driver.quit()