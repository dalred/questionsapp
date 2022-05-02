import datetime
from marshmallow import Schema, EXCLUDE
from marshmallow.fields import Int, DateTime, Str


class QuestionSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = Int(dump_only=True)  # Пропускаем поле id для дессерилиазации(для load)
    api_question_id = Int(load_only=True, data_key='id')
    created_at = DateTime(load_default=datetime.datetime.now())
    question = Str()
    answer = Str()
