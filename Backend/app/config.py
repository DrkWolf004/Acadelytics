import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DATABASE')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    COOKIE_KEY = os.getenv('cookieKey')
