from main import full_name

def test_full_name_correct():
    assert full_name("John", "Doe") == "JohnDoe"

def test_full_name_empty():
    assert full_name("", "Doe") == "Doe"

def test_full_name_another():
    assert full_name("Anna", "Smith") == "AnnaSmith"

def test_full_name_correct():
  assert full_name("Amina", " Smith") == "Amina Smith"