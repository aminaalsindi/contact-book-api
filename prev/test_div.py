from main import div
import pytest

def test_divide():
    x = 10
    y = 1

    res = div(x, y)

    assert res == 10


def test_byzero():
    x = 10
    y = 0

    with pytest.raises(ValueError):
        div(x, y)