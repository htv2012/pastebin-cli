import pathlib
import tomllib

EMPTY_CONFIG = """
api_dev_key = ""
api_user_key = ""
"""


class ConfigError(BaseException):
    pass


def load():
    """Retrieves the configurations from a file"""
    config_filename = pathlib.Path("~/.config/pastebin.toml").expanduser()
    if not config_filename.exists():
        with open(config_filename, "w") as stream:
            stream.write(EMPTY_CONFIG)
            raise ConfigError(f"Please add keys to {config_filename}")

    with open(config_filename, "rb") as stream:
        config = tomllib.load(stream)

    if "api_dev_key" not in config or "api_user_key" not in config:
        raise ConfigError(f"One or more keys are empty. Please edit {config_filename}")

    return config
