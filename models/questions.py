import datetime
from dataclasses import dataclass, field

from setup_db import db


@dataclass
class Question(db.Model):
    api_question_id: int
    created_at: datetime.datetime
    question: str
    answer: str  # = field(default=None)

    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api_question_id = db.Column(db.Integer, unique=True)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"
                                                                                                  ".%fZ"))
    question = db.Column(db.Text)
    answer = db.Column(db.Text, default=None)
