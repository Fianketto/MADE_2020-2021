from textwrap import dedent
from argparse import Namespace

import io
import pytest

from task_gadzhily_orkhan_stackoverflow_analytics import *


TEST_QUESTIONS_FPATH = "testfile_orkhan_stackoverflow_posts_sample.xml"
TEST_STOP_WORDS_FPATH = "testfile_orkhan_stop_words_en_koi8-r.txt"
TEST_QUERIES_FPATH = "testfile_orkhan_queries.csv"


def test_can_import_inv_index():
    import task_gadzhily_orkhan_stackoverflow_analytics


def test_can_load_posts():
    pop_index = get_data(TEST_QUESTIONS_FPATH, set())
    etalon_dict = {
        2008: {
                "how": 18,
                "to": 18,
                "manually": 18,
                "test": 18,
                "a": 18,
                "program": 18
        }
    }
    assert etalon_dict == pop_index.data, (
            "get_data incorrectly loaded dataset"
    )


def test_can_load_stop_words():
    stop_words = get_stop_words(TEST_STOP_WORDS_FPATH)
    etalon_set = {"a", "an"}
    assert etalon_set == stop_words, (
            "get_stop_words incorrectly loaded dataset"
    )


def test_can_load_posts_and_ignore_stop_words():
    stop_words = get_stop_words(TEST_STOP_WORDS_FPATH)
    pop_index = get_data(TEST_QUESTIONS_FPATH, stop_words)
    etalon_dict = {
        2008: {
                "how": 18,
                "to": 18,
                "manually": 18,
                "test": 18,
                "program": 18
        }
    }
    assert etalon_dict == pop_index.data, (
            "stop words were not applied correctly"
    )


@pytest.fixture()
def pop_index_tiny():
    stop_words = get_stop_words(TEST_STOP_WORDS_FPATH)
    pop_index_tiny = get_data(TEST_QUESTIONS_FPATH, stop_words)
    return pop_index_tiny


@pytest.mark.parametrize(
    "query, etalon_answer",
    [
        pytest.param(
            (2008, 2009, 3), {
            "start": 2008,
            "end": 2009,
            "top":  [
                        ["how", 18],
                        ["manually", 18],
                        ["program", 18],
                    ]
            }, id="top3 in 2008-2009"),
        pytest.param(
            (2008, 2008, 9), {
            "start": 2008,
            "end": 2008,
            "top":  [
                        ["how", 18],
                        ["manually", 18],
                        ["program", 18],
                        ["test", 18],
                        ["to", 18]
                    ]
            }, id="top9 in 2008-2008"),
        pytest.param(
            (2007, 2007, 3), {
            "start": 2007,
            "end": 2007,
            "top": []
            }, id="top3 in 2007-2007"),

    ],
)
def test_query_popularity_index(pop_index_tiny, query, etalon_answer):
    response = pop_index_tiny.query(*query)
    assert response == etalon_answer, (
        f"Expected answer is {etalon_answer}, but you got {response}"
    )


def test_can_query_from_file(pop_index_tiny, capsys):
    pop_index_tiny.queries_from_file(TEST_QUERIES_FPATH)
    etalon_response = '{"start": 2008, "end": 2008, "top": [["how", 18], ["manually", 18]]}'
    captured = capsys.readouterr()
    assert etalon_response in captured.out
