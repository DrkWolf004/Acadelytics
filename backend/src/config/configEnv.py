import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
DB_USERNAME = os.getenv('DB_USERNAME') or os.getenv('DB_USER')
PASSWORD = os.getenv('PASSWORD') or os.getenv('DB_PASSWORD')
DATABASE = os.getenv('DATABASE') or os.getenv('DB_NAME')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
DB_HOST = os.getenv('DB_HOST') or os.getenv('HOST')
cookieKey = os.getenv('cookieKey') or os.getenv('COOKIE_KEY')