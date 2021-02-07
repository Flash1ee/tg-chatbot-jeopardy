import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "configs" / "rest.yaml"


def get_config(path):
    with open(path) as file:
        parsed_config = yaml.safe_load(file)
    return parsed_config


config = get_config(config_path)