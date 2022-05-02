from abc import ABC
from typing import Optional, Any

import marshmallow
import marshmallow_dataclass


class Base_data(ABC):
    """
    Базовый класс который отвечает за получение схемы, dump схемы
    Иными словами класс позволяет получить данные в формате json,
    и отдать их в формате объекта db.model(dataclass)
    dump позволяет получить данные в формате объекта db.model(dataclass)
    и преобразовать в json
    """
    def __init__(self, object_dataclass):
        self.get_schema = self.__get_schema(object_dataclass)

    def __get_schema(self, object_dataclass):
        schema = marshmallow_dataclass.class_schema(object_dataclass)
        return schema()

    def load_schema(self, data: dict, many: Optional[bool] = None):
        try:
            return self.get_schema.load(data, many=many)
        except marshmallow.exceptions.ValidationError:
            raise ValueError

    def dump_schema(self, obj: Any, many: Optional[bool] = None):
        return self.get_schema.dump(obj=obj, many=many)
