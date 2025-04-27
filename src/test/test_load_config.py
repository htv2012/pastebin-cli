import pathlib

import pytest

from pastebin_cli.config import ConfigError, load

CONFIG_PATH = pathlib.Path("~/.config/pastebin.toml").expanduser()
BAK = CONFIG_PATH.with_suffix(".bak")
CONFIG_EXISTS = CONFIG_PATH.exists()


# ======================================================================
# Setup/teardown
# ======================================================================
def setup_module():
    if CONFIG_EXISTS:
        BAK.write_text(CONFIG_PATH.read_text())


def teardown_module():
    if CONFIG_EXISTS:
        CONFIG_PATH.write_text(BAK.read_text())


# ======================================================================
# Tests
# ======================================================================
def test_non_existent():
    CONFIG_PATH.unlink(missing_ok=True)
    with pytest.raises(ConfigError, match="Please add key"):
        load()


@pytest.mark.parametrize(
    ["config"],
    [
        pytest.param("", id="missing_both"),
        pytest.param('api_dev_key = "foo"', id="missing_api_user_key"),
        pytest.param('api_user_key = "bar"', id="missing_api_dev_key"),
        pytest.param('api_user_key = ""\ndev_user_key = ""', id="empty_keys"),
    ],
)
def test_missing_keys(config):
    CONFIG_PATH.write_text(config)
    with pytest.raises(ConfigError):
        load()


def test_happy_path():
    CONFIG_PATH.write_text('api_dev_key = "foo"\napi_user_key = "bar"')
    config = load()
    assert config == {
        "api_dev_key": "foo",
        "api_user_key": "bar",
    }
