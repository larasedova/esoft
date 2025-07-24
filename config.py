import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Базовый класс конфигурации
class Config:
    # Безопасность
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

    # База данных
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:12345678@localhost:5432/analytics_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Загрузка файлов
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Визуализация (исправленный путь для Windows)
    MATPLOTLIB_FONT_CACHE = os.path.join(os.environ.get('TEMP', os.getcwd()), 'matplotlib')

    # Автоматическое создание папок при инициализации
    @staticmethod
    def init_app(app):
        # Создаем папку для загрузок
        upload_path = Path(app.config['UPLOAD_FOLDER'])
        upload_path.mkdir(parents=True, exist_ok=True)

        # Создаем папку для кэша matplotlib
        cache_path = Path(app.config['MATPLOTLIB_FONT_CACHE'])
        cache_path.mkdir(parents=True, exist_ok=True)


# Конфигурация для разработки
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Логирование SQL-запросов


# Конфигурация для production
class ProductionConfig(Config):
    DEBUG = False
    UPLOAD_FOLDER = '/var/uploads'
    MATPLOTLIB_FONT_CACHE = '/var/cache/matplotlib'


# Конфигурация для тестирования
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Словарь для удобного выбора конфигурации
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}