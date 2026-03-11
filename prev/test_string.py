from main import find_word

def test_find_word():
    assert find_word("Amina went to the store","store")==True

def test_find_word():
    assert find_word("Amina went to the store","stoore")==False