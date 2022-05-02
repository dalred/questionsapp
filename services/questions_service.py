import requests
from flask import jsonify, request
from marshmallow import ValidationError
from exceptions import UnknownField
from helpers.functions import set_keys
from services.base_service import BaseService

from models.schemas import QuestionSchema

questionschema = QuestionSchema()
questionsschema = QuestionSchema(many=True)

import os
from config import BASEDIR

path = os.path.join(BASEDIR, 'data')


class QuestionsService(BaseService):
    """
    Класс отвечающий за сервис класс questions_models
    """

    def create_questions(self) -> jsonify:
        req_json = request.json
        models = []
        number = req_json.get('questions_num', 1)
        while number > 0:
            try:
                url = f'https://jservice.io/api/random?count={number}'
                res = requests.get(url)
                data = questionsschema.load(res.json())
            except ValidationError as e:
                raise UnknownField(message=e.normalized_messages())
            models = self.modeldao.create_many(data)
            number = number - len(models)
        return questionschema.dump(models[-1])  # Возвращаем последний вопрос

    def update_question(self, data: dict, id: int) -> jsonify:
        try:
            data = questionschema.load(data)
        except ValidationError as e:
            raise UnknownField(message=e.normalized_messages())
        update = super().update(id)
        set_keys(data, update)
        self.modeldao.update(update)
        return jsonify({"location": f'/question/{update.id}'})

    def get_all_questions(self) -> dict:
        questions_models = super().get_all_models()
        return questionsschema.dump(questions_models)

    def get_question_by_id(self, id: int) -> dict:
        questions_models = super().get_item_by_id(id)
        return questionschema.dump(questions_models)
