import pytest
from main import add_item, remove_item, mark_completed, set_priority


@pytest.fixture
def todo_list():
    return [
        {"name": "task1", "status": "pending", "priority": "low"},
        {"name": "task2", "status": "pending", "priority": "medium"},
    ]


@pytest.fixture
def empty_list():
    return []

# ---- ADD ----

@pytest.mark.parametrize("name,priority", [
    ("task3", "low"),
    ("task4", "high")
])
def test_add_item(todo_list, name, priority):
    count_before = len(todo_list)
    add_item(todo_list, name, priority)
    assert len(todo_list) == count_before + 1


# ---- REMOVE ----

def test_remove_item(todo_list):
    count_before = len(todo_list)
    remove_item(todo_list, "task1")
    assert len(todo_list) == count_before - 1


def test_remove_another(todo_list):
    count_before = len(todo_list)
    remove_item(todo_list, "task2")
    assert len(todo_list) == count_before - 1


# ---- COMPLETE ----

def test_mark_completed(todo_list):
    mark_completed(todo_list, "task1")
    assert todo_list[0]["status"] == "completed"


def test_mark_completed_second(todo_list):
    mark_completed(todo_list, "task2")
    assert todo_list[1]["status"] == "completed"


# ---- PRIORITY ----

def test_set_priority(todo_list):
    set_priority(todo_list, "task1", "high")
    assert todo_list[0]["priority"] == "high"


def test_invalid_priority(todo_list):
    with pytest.raises(ValueError):
        set_priority(todo_list, "task1", "urgent")