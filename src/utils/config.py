import json


def get_config_json(json_file: str) -> dict:
    with open(json_file, 'r') as config_file:
        config_dict = json.load(config_file)

    return config_dict
