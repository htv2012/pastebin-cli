import pathlib

import tomllib


def load():
    """Retrieves the configurations from a file"""
    config_filename = pathlib.Path("~/.config/pastebin.toml").expanduser()
    if not config_filename.exists():
        # TODO: Create the config file and ask the user to fill in
        raise SystemExit(f"Cannot find configuration file {config_filename}")

    with open(config_filename, "rb") as stream:
        config = tomllib.load(stream)

    return config
