from app.login.login_automation import LoginModule
from app.scrap.dynamic_scrap import Scrapper
from config import Config

def test_login_scrap():
    scrap = Scrapper(Config.BASE_URL, Config.EMAIL, Config.get_otp)
    try:
        driver = scrap.scrap_homepage()
        print("Inspect the browser manually if needed.")
        input("Press Enter to close the browser...")  # Keeps the browser open for debugging
    except Exception as e:
        print(f"Error: {e}")
    finally:
        scrap.close()

if __name__ == "__main__":
    test_login_scrap()