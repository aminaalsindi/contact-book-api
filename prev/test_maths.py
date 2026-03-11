from main import power, modulo, average
import pytest


def test_power():
    x = 2
    y = 3
    res = power(x, y)
    assert res == 8


def test_power_negative():
    x = 2
    y = -1
    with pytest.raises(ValueError):
        power(x, y)


def test_modulo():
    x = 10
    y = 3
    res = modulo(x, y)
    assert res == 1


def test_modulo_zero():
    x = 10
    y = 0

    with pytest.raises(ValueError):
        modulo(x, y)


def test_average():
    numbers = [2, 4, 6]
    res = average(numbers)
    assert res == 4


def test_average_empty():
    numbers = []

    with pytest.raises(ValueError):
        average(numbers)