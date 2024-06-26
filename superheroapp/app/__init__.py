import os
from flask import Flask
from .database import db
from .routes import create_routes  # Импорт функции создания маршрутов


def create_app():
    app = Flask(__name__)
    # Устанавливаем секретный ключ для сессии 
    app.secret_key = os.urandom(24)  # Не для продакшена. Данные сессии можно хранить в Redis.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        app = create_routes(app)  # Добавление маршрутов к приложению

    return app
