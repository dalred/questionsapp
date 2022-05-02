from flask import jsonify
from flask_restx import abort


# class ItemNotFound(Exception):
#
#     def abort_message(self, message: str, code: int):
#         return jsonify(abort(code, message=message))
#
#     def __str__(self):
#         return self.abort_message

class ItemNotFound(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class UnknownField(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
