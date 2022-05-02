import base64
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
class BaseConfig:
    SECRET_KEY = "test"
    JSON_AS_ASCII = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_HERE = 'test'

    TOKEN_EXPIRE_MINUTES ="test"
    TOKEN_EXPIRE_DAYS = "test"

    PWD_HASH_SALT = base64.b64decode("salt")
    PWD_HASH_ITERATIONS = 100_000
    JSON_PATH = os.path.join(
        os.path.dirname(BASEDIR), "test"
    )

class TestingConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.normpath(os.path.join(
        BASEDIR, "database/project.db")
    )
    JSON_SORT_KEYS = False

class PostgresConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://flaskappuserdb:dalprodal123@postgres:5432/questions'
    JSON_SORT_KEYS = False