import json
import os

import dotenv
import requests
from flask import request, jsonify
from flask_restx import abort, Namespace, Resource
from helpers.functions import get_user_access_token, dotenv_file

hh_ns = Namespace("hh")


@hh_ns.route("/")
class QuestionsView(Resource):
    def get(self):
        access_token = os.getenv('access_token')
        if not access_token:
            state = request.args.get('state')
            auth_code = request.args.get('code')
            access_token, refresh_token, acc_token_expire = get_user_access_token(auth_code, state)
            os.environ["access_token"] = access_token
            os.environ["refresh_token"] = refresh_token
            os.environ["acc_token_expire"] = str(acc_token_expire)
            os.environ["auth_code"] = auth_code
            dotenv.set_key(dotenv_file, "access_token", os.environ["access_token"])
            dotenv.set_key(dotenv_file, "refresh_token", os.environ["refresh_token"])
            dotenv.set_key(dotenv_file, "acc_token_expire", os.environ["acc_token_expire"])
            dotenv.set_key(dotenv_file, "auth_code", os.environ["auth_code"])
        header = {'Authorization': f'Bearer {access_token}'}
        resp = requests.get('https://api.hh.ru/negotiations', headers=header)
        return jsonify(resp.json())
