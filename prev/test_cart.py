import pytest
from main import add_item, remove_item, get_total, apply_discount

@pytest.fixture
def empty_cart():
    return []

@pytest.fixture
def cart_with_items():
    return [
        {"item": "apple", "price": 2},
        {"item": "bread", "price": 3},
        {"item": "cheese", "price": 5}
    ]

def test_add_item(empty_cart):
    add_item(empty_cart, "apple", 2)
    assert len(empty_cart) == 1


def test_add_multiple_items(empty_cart):
    add_item(empty_cart, "apple", 2)
    add_item(empty_cart, "bread", 3)
    assert len(empty_cart) == 2


def test_remove_item(cart_with_items):
    remove_item(cart_with_items, "bread")
    assert len(cart_with_items) == 2


def test_remove_specific_item(cart_with_items):
    remove_item(cart_with_items, "apple")
    assert cart_with_items[0]["item"] != "apple"


def test_get_total(cart_with_items):
    assert get_total(cart_with_items) == 10


def test_get_total_after_add(empty_cart):
    add_item(empty_cart, "bread", 4)
    add_item(empty_cart, "cheese", 6)
    assert get_total(empty_cart) == 10


def test_discount_10(cart_with_items):
    assert apply_discount(cart_with_items, 10) == 9


def test_discount_20(cart_with_items):
    assert apply_discount(cart_with_items, 20) == 8


def test_discount_zero(cart_with_items):
    assert apply_discount(cart_with_items, 0) == 10


def test_discount_full(cart_with_items):
    assert apply_discount(cart_with_items, 100) == 0