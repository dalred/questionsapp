from typing import Any

from flask import jsonify
from sqlalchemy.orm.scoping import scoped_session
from flask_restx import abort
from exceptions import ItemNotFound
from helpers.functions import set_keys


class BaseService:
    """
    Класс базовый сервис, наверное существуют разные пути обработки ошибок
    кто-то обрабатывает ошибки на уровне базы, а кто-то на уровне сервиса,
    мы решили обрабатывать на уровне сервиса, возможно нужно это делать и на уровне
    DAO и на уровне сервиса.
    """
    def __init__(self, session: scoped_session, modeldao: Any) -> None:
        self._db_session = session
        self.modeldao = modeldao
        self.name = self.modeldao.__class__.__name__

    def get_item_by_id(self, uid: int) -> Any:
        model = self.modeldao.get_by_id(uid)
        if not model:
            raise ItemNotFound(f"id equal {uid} in {self.name} not found!")
        return model

    def get_all_models(self) -> Any:
        models = self.modeldao.get_all()
        return models

    def create_model(self, data: dict) -> Any:
        models = self.modeldao.create(data)
        return models

    # Готовим update и только потом передаем в базу, решил на уровне базы не возится с data
    def update(self, uid: int) -> Any:
        return self.get_item_by_id(uid)

    #Cначала проверим на уровне сервиса и только потом запустим удаление.
    def delete(self, uid: int) -> None:
        model = self.get_item_by_id(uid)
        self.modeldao.delete(model)
