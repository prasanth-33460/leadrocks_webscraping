from app.login.login_automation import LoginModule
from config import Config

def test_login():
    login_module = LoginModule(Config.BASE_URL, Config.EMAIL, Config.get_otp)

    try:
        driver = login_module.login()
        print("Inspect the browser manually if needed.")
        input("Press Enter to close the browser...")  # Keeps the browser open for debugging
    except Exception as e:
        print(f"Error: {e}")
    finally:
        login_module.close()

if __name__ == "__main__":
    test_login()
