from typing import Any

import requests
from flask import jsonify, request
from marshmallow import ValidationError, INCLUDE, RAISE
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
    Класс QuestionsService отвечающий за сервис то есть за бизнес логику
    """

    def create_questions(self) -> dict:
        req_json = request.json
        models = []
        number_attemp = 0
        number = req_json.get('questions_num', 1)
        while number > 0:
            try:
                if number_attemp == 50:  # Не больше 50 попыток
                    number = 0
                url = f'https://jservice.io/api/random?count={number}'
                res = requests.get(url)
                data = questionsschema.load(res.json())
            except ValidationError as e:
                raise UnknownField(message=e.normalized_messages())
            models = self.modeldao.create_many(data)
            number = number - len(models)
            number_attemp += 1
        print(f'number_attemp:{number_attemp}')
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

    def create_question(self, data) -> dict:
        try:
            data = questionschema.load(data, unknown=RAISE)
            """
            RAISE (default): raise a ValidationError if there are any unknown fields
            INCLUDE: accept and include the unknown fields
            """
        except ValidationError as e:
            raise UnknownField(message=e.normalized_messages())
        question_model = super().create_model(data=data)
        return questionschema.dump(question_model)
