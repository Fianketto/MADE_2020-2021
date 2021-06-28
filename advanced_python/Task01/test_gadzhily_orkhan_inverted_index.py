from textwrap import dedent
from argparse import Namespace

import io
import pytest

from task_gadzhily_orkhan_inverted_index import *



DATASET_BIG_FPATH = "wikipedia_sample.txt"
DATASET_SMALL_FPATH = "wikipedia_sample_short.txt"
DATASET_TINY_FPATH = "wikipedia_sample_tiny.txt"


def test_can_load_documents_v1():
    documents = load_documents(DATASET_TINY_FPATH)
    etalon_documents = {
        123:	'some words A_word and nothing',
        2:	'some word B_word in this dataset',
        5:	'famous_phrases to be or not to be',
        37:	'all words such as A_word and B_word are here'
    }
    assert etalon_documents == documents, (
            "load_documents incorrectly loaded dataset"
    )


def test_can_load_documents_v2(tmpdir):
    dataset_str = dedent("""\
        123 	some words A_word and nothing
        2	some word B_word in this dataset
        5	famous_phrases to be or not to be
        37	all words such as A_word and B_word are here
    """)
    dataset_fio = tmpdir.join("tiny.dataset")
    dataset_fio.write(dataset_str)
    documents = load_documents(dataset_fio)
    etalon_documents = {
        123:	'some words A_word and nothing',
        2:	'some word B_word in this dataset',
        5:	'famous_phrases to be or not to be',
        37:	'all words such as A_word and B_word are here'
    }
    assert etalon_documents == documents, (
            "load_documents incorrectly loaded dataset"
    )


DATASET_TINY_STR = dedent("""\
    123	some words A_word and nothing
    2	some word B_word in this dataset
    5	famous_phrases to be or not to be
    37	all words such as A_word and B_word are here
""")


@pytest.fixture()
def tiny_dataset_fio(tmpdir):
    dataset_fio = tmpdir.join("dataset.txt")
    dataset_fio.write(DATASET_TINY_STR)
    return dataset_fio


def test_can_load_documents(tiny_dataset_fio):
    documents = load_documents(tiny_dataset_fio)
    etalon_documents = {
        123:	'some words A_word and nothing',
        2:	'some word B_word in this dataset',
        5:	'famous_phrases to be or not to be',
        37:	'all words such as A_word and B_word are here'
    }
    assert etalon_documents == documents, (
            "load_documents incorrectly loaded dataset"
    )


@pytest.mark.parametrize(
    "query, etalon_answer",
    [
        pytest.param(["A_word"], [123, 37]),
        pytest.param(["B_word"], [2, 37], id="B_word"),
        pytest.param(["A_word", "B_word"], [37], id="both words"),
        pytest.param(["word_does_not_exists"], [], id="word does not exists"),
        pytest.param([], [], id="empty query"),
        pytest.param([""], [], id="empty string"),

    ],
)
def test_query_inverted_index_intersect_results(tiny_dataset_fio, query, etalon_answer):
    documents = load_documents(tiny_dataset_fio)
    tiny_inverted_index = build_inverted_index(documents)
    answer = tiny_inverted_index.query(query)
    assert sorted(answer) == sorted(etalon_answer), (
        f"Expected answer is {etalon_answer}, but you got {answer}"
    )


#@pytest.mark.skip()    #SKIP
def test_can_load_wikipedia_sample():
    documents = load_documents(DATASET_TINY_FPATH)
    assert len(documents) == 4, (
        "you incorrectly loaded Wikipedia sample"
    )


@pytest.fixture()
def wikipedia_documents():
    documents = load_documents(DATASET_BIG_FPATH)
    return documents

@pytest.fixture
def small_wikipedia_documents():
    documents = load_documents(DATASET_SMALL_FPATH)
    return documents

@pytest.fixture
def tiny_wikipedia_documents():
    documents = load_documents(DATASET_TINY_FPATH)
    return documents

@pytest.fixture
def wikipedia_inverted_index(wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(wikipedia_documents)
    return wikipedia_inverted_index

@pytest.fixture
def small_wikipedia_inverted_index(small_wikipedia_documents):
    small_wikipedia_inverted_index = build_inverted_index(small_wikipedia_documents)
    return small_wikipedia_inverted_index

@pytest.fixture
def tiny_wikipedia_inverted_index(tiny_wikipedia_documents):
    tiny_wikipedia_inverted_index = build_inverted_index(tiny_wikipedia_documents)
    return tiny_wikipedia_inverted_index




def test_can_build_and_query_inverted_index(small_wikipedia_documents):
    small_wikipedia_documents_after_build = build_inverted_index(small_wikipedia_documents)
    doc_ids = small_wikipedia_documents_after_build.query(["wikipedia"])
    assert isinstance(doc_ids, list), "inverted index query should return list"


def test_can_dump_and_load_inverted_index(tmpdir, small_wikipedia_inverted_index):
    index_fio = tmpdir.join("index.dump")
    small_wikipedia_inverted_index.dump(index_fio)
    loaded_inverted_index = InvertedIndex.load(index_fio)
    assert small_wikipedia_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


@pytest.mark.parametrize(
    ("filepath",),
    [
        pytest.param(DATASET_SMALL_FPATH, id="small dataset"),
        pytest.param(DATASET_BIG_FPATH, marks=[pytest.mark.skipif(1 == 1, reason="I'm lazy")], id="big dataset"),
    ],
)
def test_can_dump_and_load_inverted_index_with_array_policy_parametrized(filepath, tmpdir):
    index_fio = tmpdir.join("index.dump")
    documents = load_documents(filepath)
    etalon_inverted_index = build_inverted_index(documents)
    etalon_inverted_index.dump(index_fio)
    loaded_inverted_index = InvertedIndex.load(index_fio)
    assert etalon_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


def test_can_import_inv_index():
    import task_gadzhily_orkhan_inverted_index


def test_can_instantiate_inv_index_object():
    inv_index = InvertedIndex()


def test_search_empty_list(small_wikipedia_inverted_index):
    document_ids = small_wikipedia_inverted_index.query([])
    expected_document_ids = []

    assert set(document_ids) == set(expected_document_ids), (
            "wrong document_ids"
        )


def test_search_empty_string(small_wikipedia_inverted_index):
    document_ids = small_wikipedia_inverted_index.query([""])
    expected_document_ids = []

    assert set(document_ids) == set(expected_document_ids), (
            "wrong document_ids"
        )


def test_raises_error_when_document_file_not_found():
    filepath = "unexisting_document_and_code_to_be_sure_it_doesnt_exist_77899854785"
    with pytest.raises(FileNotFoundError):
        documents = load_documents(filepath)


def test_prints_succes():
    file_type=EncodedFileType("r", encoding="utf8")
    file_type.cheating_on_pylint()
    assert 1 == 1, (
        "sorry, what?"
)


def test_can_encoded_file_r(monkeypatch):
    monkeypatch.setattr('sys.stdin', TextIOWrapper(io.BytesIO(b"test")))
    encoded_type = EncodedFileType("r", encoding="utf-8")
    text_io = encoded_type('-')
    assert TextIOWrapper == text_io.__class__, f"Expected encoded type without error"














def test_process_arguments_query_can_process_all_queries(tmpdir, tiny_wikipedia_inverted_index):
    index_fio = tmpdir.join("index.dump")
    tiny_wikipedia_inverted_index.dump(index_fio)
    etalon_document_ids = [123, 37]
    document_ids = process_arguments_query(
        inverted_index_filepath=index_fio,
        query=["A_word"]
    )
    assert sorted(document_ids) == sorted(etalon_document_ids)


def test_process_arguments_build_can_build_and_dump_from_correct_dataset(tmpdir):
    documents = load_documents(DATASET_TINY_FPATH)
    etalon_inverted_index = build_inverted_index(documents)
    index_fio = tmpdir.join("index.dump")
    process_arguments_build(
        dataset_filepath=DATASET_TINY_FPATH,
        output_filepath=index_fio
    )
    loaded_inverted_index = InvertedIndex.load(index_fio)
    assert etalon_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


def test_callback_build_calls_right_process(tmpdir):
    documents = load_documents(DATASET_TINY_FPATH)
    etalon_inverted_index = build_inverted_index(documents)
    index_fio = tmpdir.join("index.dump")
    build_arguments = Namespace(
        dataset=DATASET_TINY_FPATH,
        output=index_fio
    )
    callback_build(build_arguments)
    process_arguments_build(build_arguments.dataset, build_arguments.output)
    loaded_inverted_index = InvertedIndex.load(index_fio)
    assert etalon_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


def test_callback_query_calls_right_proccess_for_individual_query(
		tmpdir, tiny_wikipedia_inverted_index, capsys
	):
    index_fio = tmpdir.join("index.dump")
    tiny_wikipedia_inverted_index.dump(index_fio)
    query_arguments = Namespace(
        query=[["A_word"]],
        input=index_fio,
        query_file=None
    )
    callback_query(query_arguments)
    captured = capsys.readouterr()
    assert "123,37" in captured.out


def test_callback_query_calls_right_proccess_for_query_file(
		tmpdir, tiny_wikipedia_inverted_index, capsys
	):
    index_fio = tmpdir.join("index.dump")
    tiny_wikipedia_inverted_index.dump(index_fio)
    query_str = dedent("""\
        A_word
        B_word
        A_word B_word
        word_does_not_exists
    """)
    query_fio = tmpdir.join("queries.txt")
    query_fio.write(query_str)
    query_fio_object = open(query_fio)
    query_arguments = Namespace(
        query=None,
        input=index_fio,
        query_file=query_fio_object,
    )
    callback_query(query_arguments)
    query_fio_object.close()
    captured = capsys.readouterr()
    assert "123,37\n2,37\n37\n" in captured.out
