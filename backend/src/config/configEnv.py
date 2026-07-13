import os
from pathlib import Path
from dotenv import load_dotenv

CONFIG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[3]

for env_path in [CONFIG_DIR / '.env', PROJECT_ROOT / '.env']:
    if env_path.exists():
        load_dotenv(env_path, encoding='utf-8')


def _parse_csv(value: str | None, fallback: str) -> list[str]:
    if not value:
        value = fallback
    return [item.strip() for item in value.split(',') if item.strip()]


PORT = os.getenv('PORT', '5000')
HOST = os.getenv('HOST', '0.0.0.0')
DB_USERNAME = os.getenv('DB_USERNAME') or os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('PASSWORD') or os.getenv('DB_PASSWORD', 'postgres')
DATABASE = os.getenv('DATABASE') or os.getenv('DB_NAME', 'acadelytics')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET') or os.getenv('JWT_SECRET') or 'supersecret_jwt_key'
DB_HOST = os.getenv('DB_HOST', 'localhost')
cookieKey = os.getenv('cookieKey') or os.getenv('COOKIE_KEY', 'supersecret_cookie')
CORS_ORIGINS = _parse_csv(
    os.getenv('CORS_ORIGINS'),
    'http://localhost:4173,http://127.0.0.1:4173,http://localhost:5173,http://127.0.0.1:5173'
)