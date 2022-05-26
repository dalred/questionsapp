import csv
import json
import os
import webbrowser

import requests
import dotenv

from rauth import OAuth2Service

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

def read_json(name: str) -> dict:
    with open(name, "r", encoding='utf-8') as file:
        return json.load(file)


def set_keys(req_json, inst_cls):
    inst_cls_keys = [key for key in inst_cls.__dict__.keys() if key != '_sa_instance_state']
    for k, v in req_json.items():
        # Проверка в принципе не нужна,
        # потому что Flask сам обработает,
        # если ключ в json отличный от схемы.
        if k in inst_cls_keys: #заглушка чтобы не менял id  and k != 'id' не нужна
            # Присвоить атрибутам новые значения
            setattr(inst_cls, k, v)

def csv_to_json(csv_file_path: str, out_path: str) -> None:
    with open(csv_file_path, encoding='utf-8') as csvf:
        jsonArray = []
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            jsonArray.append(row)
    json_name = os.path.basename(csv_file_path).replace('.csv', '.json')
    out_path = os.path.join(out_path, json_name)
    with open(out_path, 'w', encoding='utf-8') as jsonf:
        json_string = json.dumps(jsonArray, indent=4, ensure_ascii=False)
        jsonf.write(json_string)

def get_user_access_token(user_code, state):
    """
    :return: {
        "access_token": "{access_token}",
        "token_type": "bearer",
        "expires_in": 1209600,
        "refresh_token": "{refresh_token}"
        }
    """
    url = 'https://hh.ru/oauth/token'

    data = {
        'grant_type': 'authorization_code',
        'client_id': os.getenv('client_id'),
        'client_secret': os.getenv("client_secret"),
        'code': user_code,
        'state': state
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 200:
        res_json = response.json()
        return res_json['access_token'], res_json['refresh_token'], res_json['expires_in']
    elif response.status_code == 400:
        print('Bad request')
    return response


def get_autorized():
    hh = OAuth2Service(
        client_id=os.getenv('client_id'),
        client_secret=os.getenv('client_secret'),
        name='Checker',
        authorize_url='https://hh.ru/oauth/authorize',
        access_token_url='https://hh.ru/oauth/token',
        base_url='https://hh.ru/')

    params = {'state': 'read_stream',
              'response_type': 'code'}
    authorize_url = hh.get_authorize_url(**params)
    webbrowser.open_new_tab(authorize_url)