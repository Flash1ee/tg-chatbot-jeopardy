import pathlib
import json

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "config.json"


def get_config(path):
    with open(path) as f:
        parsed_config = json.load(f)
    return parsed_config


cfg = get_config(config_path)