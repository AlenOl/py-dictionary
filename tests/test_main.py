from unittest import mock

import pytest

from app.main import Dictionary
from app.point import Point


@pytest.mark.parametrize(
    "items,pairs_after_adding",
    [
        pytest.param([], [], id="empty dictionary should have len equal to 0"),
        pytest.param(
            [(1, "one"), (2, "two"), (3, "tree"), (4, "four")],
            [(1, "one"), (2, "two"), (3, "tree"), (4, "four")],
            id="integers can be used as keys",
        ),
        pytest.param(
            [(1.1, "one"), (2.2, "two"), (3.3, "tree"), (4.4, "four")],
            [(1.1, "one"), (2.2, "two"), (3.3, "tree"), (4.4, "four")],
            id="floats can be used as keys",
        ),
        pytest.param(
            [("one", 1), ("two", 2), ("tree", 3), ("four", 4)],
            [("one", 1), ("two", 2), ("tree", 3), ("four", 4)],
            id="strings can be used as keys",
        ),
        pytest.param(
            [
                (Point(0, 0), "origin"),
                (Point(10, 10), "A"),
                (Point(-10, 10), "B"),
                (Point(0, 5), "C"),
            ],
            [
                (Point(0, 0), "origin"),
                (Point(10, 10), "A"),
                (Point(-10, 10), "B"),
                (Point(0, 5), "C"),
            ],
            id="Custom hashable classes can be used as keys",
        ),
        pytest.param(
            [("one", 1), (2, [1, 2, 3]), (13.3, 66), (Point(0, 0), "origin")],
            [("one", 1), (2, [1, 2, 3]), (13.3, 66), (Point(0, 0), "origin")],
            id="keys can have different hashable types",
        ),
        pytest.param(
            [
                (8, "8"),
                (16, "16"),
                (32, "32"),
                (64, "64"),
                (128, "128"),
                ("one", 2),
                ("two", 2),
                (Point(1, 1), "a"),
                ("one", 1),
                ("one", 11),
                ("one", 111),
                ("one", 1111),
                (145, 146),
                (145, 145),
                (145, -1),
                ("two", 22),
                ("two", 222),
                ("two", 2222),
                ("two", 22222),
                (Point(1, 1), "A"),
            ],
            [
                (8, "8"),
                (16, "16"),
                (32, "32"),
                (64, "64"),
                (128, "128"),
                ("one", 1111),
                ("two", 22222),
                (145, -1),
                (Point(1, 1), "A"),
            ],
            id="the value should be reassigned when the key already exists",
        ),
    ],
)
@mock.patch("app.main.hash")
def test_dictionary_add(mock_hash: mock, items: list, pairs_after_adding: list):
    mock_hash.return_value = 3

    dictionary = Dictionary()
    for key, value in items:
        dictionary[key] = value

    for key, value in pairs_after_adding:
        assert dictionary[key] == value
    assert len(dictionary) == len(pairs_after_adding)


@pytest.mark.timeout(5)
def test_resize_bucket():
    items = [(f"Element {i}", i) for i in range(1000)]
    dictionary = Dictionary()
    for key, value in items:
        dictionary[key] = value

    for key, value in items:
        assert dictionary[key] == value
    assert len(dictionary) == len(items)


def test_missing_key():
    dictionary = Dictionary()
    with pytest.raises(KeyError):
        dictionary["missing_key"]
