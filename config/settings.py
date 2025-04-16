import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ASSISTANT_ID = os.getenv("ASSISTANT_ID")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Database Config
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_EXPIRATION_TIME = os.getenv("JWT_EXPIRATION_TIME", default=1)  # Default to 1 hour if not set
    
    # Flask Config
    CORS_SETTINGS = {
        'supports_credentials': True,
        'resources': {r"/*": {"origins": "*"}}
    }
    
    SESSION_COOKIE_SETTINGS = {
        'SAMESITE': "None",
        'SECURE': True,
        'PERMANENT_SESSION_LIFETIME': timedelta(minutes=30),
        'SESSION_PERMANENT': True 
    }