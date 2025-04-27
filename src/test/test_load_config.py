import pathlib

import pytest

from pastebin_cli.config import ConfigError, load

CONFIG_PATH = pathlib.Path("~/.config/pastebin.toml").expanduser()
BAK = CONFIG_PATH.with_suffix(".bak")


def setup_module():
    BAK.write_text(CONFIG_PATH.read_text())


def teardown_module():
    CONFIG_PATH.write_text(BAK.read_text())


def test_non_existent():
    CONFIG_PATH.unlink(missing_ok=True)

    with pytest.raises(ConfigError, match="Please add key"):
        load()


@pytest.mark.parametrize(
    ["config", "raise_context"],
    [
        pytest.param("", pytest.raises(ConfigError), id="no_keys"),
        pytest.param(
            'api_dev_key = "foo"', pytest.raises(ConfigError), id="missing_api_user_key"
        ),
        pytest.param(
            'api_user_key = "bar"', pytest.raises(ConfigError), id="missing_api_dev_key"
        ),
        pytest.param(
            'api_user_key = ""\ndev_user_key = ""',
            pytest.raises(ConfigError),
            id="empty_keys",
        ),
    ],
)
def test_missing_keys(config, raise_context):
    CONFIG_PATH.write_text(config)
    with raise_context:
        load()


def test_happy_path():
    CONFIG_PATH.write_text('api_dev_key = "foo"\napi_user_key = "bar"')
    config = load()
    assert config == {
        "api_dev_key": "foo",
        "api_user_key": "bar",
    }
