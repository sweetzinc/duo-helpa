import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    TARGET_LANGUAGE = os.getenv('TARGET_LANGUAGE', 'German')
    SOURCE_LANGUAGE = os.getenv('SOURCE_LANGUAGE', 'English')
    
    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Please set it in your .env file.")
        return True