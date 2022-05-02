import os
from config import BASEDIR
from dao.QuestionDAO import QuestionDAO
from models import Question
from helpers import read_json
from services.questions_service import QuestionsService
from setup_db import db

path = os.path.join(BASEDIR, 'data')
questions_dict: dict = read_json(f'{path}/questions.json')

questions = QuestionDAO(db.session, Question)
question_service = QuestionsService(db.session, questions)