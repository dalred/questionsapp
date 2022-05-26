from typing import Any

from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
from config import DevelopmentConfig, PostgresConfig

from helpers.create_tables import create_tables

from setup_db import db
from views.hh_view import hh_ns
from views.question_view import questions_ns


def create_app(config_object: Any) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)
    # app.config.from_envvar('APP_SETTINGS', silent=True)
    register_extensions(app)
    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    api = Api(app)
    api.add_namespace(questions_ns)
    #api.add_namespace(hh_ns)
    create_data(app)


def create_data(app: Flask) -> None:
    with app.app_context():
        create_tables()


app = create_app(DevelopmentConfig)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run('127.0.0.1', 10001)
