import json

from flask import request, jsonify
from flask_restx import abort, Namespace, Resource
import requests
from exceptions import ItemNotFound, UnknownField
from implemented import question_service
from models.schemas import QuestionSchema

questionschema = QuestionSchema()
questionsschema = QuestionSchema(many=True)
questions_ns = Namespace("questions")

@questions_ns.route("/ask/")
class QuestionsView(Resource):
    def post(self):
        """Create questions"""
        try:
            return question_service.create_questions()
        except UnknownField as e:
            abort(502, message=e.message)

@questions_ns.route("/")
class QuestionsView(Resource):
    @questions_ns.response(200, "OK")
    def get(self):
        """Get all questions"""
        return question_service.get_all_questions()

    def post(self):
        """Create question"""
        req_json = request.json
        try:
            return question_service.create_question(req_json)
        except UnknownField as e:
            abort(502, message=e.message)

@questions_ns.route('/<int:id>/')
class QuestionView(Resource):
    @questions_ns.response(200, "OK")
    @questions_ns.response(404, "question not found")
    def get(self, id: int):
        try:
            return question_service.get_question_by_id(id)
        except ItemNotFound as e:
            abort(404, message=e.message)

    def patch(self, id: int):
        req_json = request.json
        try:
            question_service.update_question(req_json, id)
        except UnknownField as e:
            abort(502, message=e.message)
        return "", 204

    def delete(self, id: int):
        try:
            question_service.delete(id)
        except ItemNotFound as e:
            abort(404, message=e.message)
        return "", 204
