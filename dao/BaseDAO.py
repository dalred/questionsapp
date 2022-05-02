from typing import Any, List
from sqlalchemy.orm.scoping import scoped_session
from sqlite3 import IntegrityError

class BaseDAO:
    def __init__(self, session: scoped_session, model):
        self._db_session = session
        self.model = model
        self.message = model.__name__

    def get_by_id(self, pk: int) -> Any:
        return self._db_session.query(self.model).filter(self.model.id == pk).one_or_none()

    def get_all(self):
        return self._db_session.query(self.model).all()

    def create(self, data: dict) -> Any:
        ent = self.model(**data)
        try:
            self._db_session.add(ent)
            self._db_session.commit()
        except IntegrityError:
            self._db_session.session.rollback()
        return ent

    def update(self, update) -> None:
        self._db_session.add(update)
        self._db_session.commit()

    def delete(self, delete) -> None:
        self._db_session.delete(delete)
        self._db_session.commit()
