import os
from dotenv import load_dotenv
from pathlib import Path

try:
    project_root = Path(__file__).resolve().parents[3]
    dotenv_path = project_root / '.env'
    if dotenv_path.exists():
        load_dotenv(dotenv_path, encoding='utf-8')
    else:
        fallback_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(fallback_path):
            load_dotenv(fallback_path, encoding='utf-8')
except Exception as e:
    print(f"Advertencia: Error cargando .env: {e}")

PORT = os.getenv('PORT', '5000')
HOST = os.getenv('HOST', '0.0.0.0')
DB_USERNAME = os.getenv('DB_USERNAME') or os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('PASSWORD') or os.getenv('DB_PASSWORD', 'postgres')
DATABASE = os.getenv('DATABASE') or os.getenv('DB_NAME', 'acadelytics')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET') or os.getenv('JWT_SECRET') or 'supersecret_jwt_key'
DB_HOST = os.getenv('DB_HOST', 'localhost')
cookieKey = os.getenv('cookieKey') or os.getenv('COOKIE_KEY', 'supersecret_cookie')