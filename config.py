import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Основные настройки
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:12345678@localhost:5432/analytics_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Настройки загрузки файлов
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Настройки matplotlib
    MATPLOTLIB_FONT_CACHE = '/tmp/matplotlib'
