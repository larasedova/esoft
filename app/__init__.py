from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Инициализация расширений
db = SQLAlchemy()


def create_app():
    # Создание экземпляра приложения
    app = Flask(__name__)
    app.config.from_object(Config)

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