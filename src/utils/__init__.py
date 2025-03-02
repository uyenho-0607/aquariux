import yaml

from src.consts import CONFIG_DIR


def load_config_data(env):
    config_file_path = CONFIG_DIR / f"{env}.yaml"
    with open(config_file_path, "r") as file:
        config_data = yaml.safe_load(file)

    return config_data
