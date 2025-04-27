import pathlib

import pytest

from pastebin_cli.filelib import get_content


@pytest.fixture()
def data():
    return "Hello, world"


@pytest.fixture(params=[str, pathlib.Path])
def data_path(request, tmp_path, data):
    path = tmp_path / "data.txt"
    path.write_text(data)
    cast = request.param
    return cast(path)


def test_get_content(data_path, data):
    actual = get_content(data_path)
    assert actual == data
