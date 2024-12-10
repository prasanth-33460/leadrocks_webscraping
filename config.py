import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    BASE_URL = "https://leadrocks.io/auth"  # Update the base URL as needed
    EMAIL = os.getenv("LEADROCKS_EMAIL", "your_email@example.com")
    # OTP Retrieval Function
    @staticmethod
    def get_otp():
        """
        Retrieve the OTP from the email.
        Replace this logic with the specific email parsing mechanism.
        """
        # Simulating OTP retrieval for now (replace with actual implementation)
        otp = input("Enter the OTP sent to your email: ")
        return otp
