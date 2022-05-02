import csv
import json
import os


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