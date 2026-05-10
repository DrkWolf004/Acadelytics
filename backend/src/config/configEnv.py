import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
DB_USERNAME = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('PASSWORD')
DATABASE = os.getenv('DATABASE')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
cookieKey = os.getenv('cookieKey')