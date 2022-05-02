from dao.BaseDAO import BaseDAO
from typing import Any, List

class QuestionDAO(BaseDAO):
    def get_by_api_question_id(self, pk: int) -> Any:
        return self._db_session.query(self.model).filter(self.model.api_question_id == pk).one_or_none()

    def create_many(self, datas: List[dict]) -> Any:
        data_model = []
        for data in datas:
            api_question_id = data.get('api_question_id', None)
            database = self.get_by_api_question_id(api_question_id)
            if not database:
                data_model.append(self.model(**data))
        self._db_session.add_all(data_model)
        self._db_session.commit()
        return data_model