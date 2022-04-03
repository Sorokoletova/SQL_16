import json

def get_open_json(file_name):
    """Получение данных из json"""
    with open(file_name, encoding='utf-8') as file:
        json_data = json.load(file)

    return json_data



