def add_item(todo_list, name, priority):
    item = {"name": name, "status": "pending", "priority": priority}
    todo_list.append(item)


def remove_item(todo_list, name):
    for item in todo_list:
        if item["name"] == name:
            todo_list.remove(item)
            break


def mark_completed(todo_list, name):
    for item in todo_list:
        if item["name"] == name:
            item["status"] = "completed"


def set_priority(todo_list, name, priority):
    if priority not in ["low", "medium", "high"]:
        raise ValueError("Invalid priority")

    for item in todo_list:
        if item["name"] == name:
            item["priority"] = priority