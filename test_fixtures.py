import pytest
from app import create_app
from app import db

@pytest.fixture
def empty_list():
    return []

@pytest.fixture
def string_value():
    return "hello"

def test_len_of_empty_list(empty_list, string_value):
    empty_list.append(string_value)
    assert isinstance(empty_list, list)
    assert len(empty_list) == 1

class FancyObject:
    def __init__(self):
        self.fancy = True
        print(f"\nFancyObject: {self.fancy}")

    def or_is_it(self):
        self.fancy = not self.fancy

    def cleanup(self):
        print(f"\ncleanup: {self.fancy}")

@pytest.fixture
def so_fancy():
    fancy_object = FancyObject()

    yield fancy_object

    fancy_object.cleanup()

def test_so_fancy(so_fancy):
    assert so_fancy.fancy
    so_fancy.or_is_it()
    assert not so_fancy.fancy