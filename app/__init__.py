from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import config  # Импортируем словарь конфигураций

# Инициализация расширений
db = SQLAlchemy()


def create_app(config_name='default'):
    """Фабрика приложений с поддержкой разных конфигураций"""
    # Создание экземпляра приложения
    app = Flask(__name__)

    # Загрузка конфигурации
    app.config.from_object(config[config_name])

    # Инициализация приложения (создание папок)
    config[config_name].init_app(app)

    # Инициализация БД
    db.init_app(app)

    # Регистрация Blueprint
    from app.routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Создание таблиц БД
    with app.app_context():
        db.create_all()

    # Обработчики ошибок
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app