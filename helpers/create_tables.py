from models.models_options.questions_options import Questions_Option
from implemented import questions_dict
from setup_db import db
from models import *

def create_tables():
    db.drop_all()
    db.create_all()
    question = Questions_Option(Question)
    question = question.load_schema(questions_dict, many=True)
    db.session.add_all(question)
    db.session.commit()
