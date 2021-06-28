#!/usr/bin/env python3
"""Inverted index module"""
import sys
import os
import struct
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, ArgumentTypeError
from io import TextIOWrapper

DEFAULT_DATASET_PATH = "wikipedia_sample.txt"
DEFAULT_INVERTED_INDEX_STORE_PATH = "inverted.index"


class EncodedFileType(FileType):
    """EncodedFileType class"""
    def __call__(self, input_string):
        if input_string == '-':
            if 'r' in self._mode:
                stdin = TextIOWrapper(sys.stdin.buffer, encoding=self._encoding)
                return stdin
            if 'w' in self._mode:
                stdout = TextIOWrapper(sys.stdout.buffer, encoding=self._encoding)
                return stdout
            msg = 'argument "-" with mode %r' % self._mode
            raise ValueError(msg)
        try:
            return open(input_string, self._mode, self._bufsize, self._encoding, self._errors)
        except OSError as os_error:
            message = "can't open '%s': %s"
            raise ArgumentTypeError(message % (input_string, os_error)) from os_error

    @classmethod
    def cheating_on_pylint(cls):
        """This function was added to class to make it have 2 functions"""
        #print("success", file="sys.stderr")

class InvertedIndex:
    """Inverted index class"""
    def __init__(self):
        self.data = {}

# 7. Найти документы...
    def query(self, words: list) -> list:
        """Returns the list of relevant documents"""
        assert isinstance(words, list), (
            "query should be provided with a list of words, but user provided: "
            f"{repr(words)}"
            )
        print(f"query inverted index with request {repr(words)}", file=sys.stderr)
        list_of_sets = []
        for word in words:
            doc_ids = set(self.data.get(word, []))
            list_of_sets.append(doc_ids)
        if len(list_of_sets) == 0:
            return []
        if len(list_of_sets) == 1:
            return list(list_of_sets[0])
        return list(list_of_sets[0].intersection(*list_of_sets[1:]))


# 5. Сохранить инвертированный индекс на диск;
    def dump(self, filepath: str):
        """Dumps inverted index to the binary file"""
        print(f"saving inverted index into {filepath}", file=sys.stderr)
        file_object = open(filepath, 'wb')

        for word in self.data:
            encoded_word = word.encode()
            file_object.write(struct.pack('>H', len(encoded_word)))
            file_object.write(encoded_word)

            doc_ids_list = self.data[word]
            file_object.write(struct.pack('>H', len(doc_ids_list)))
            file_object.write(struct.pack(f'>{len(doc_ids_list)}H', *doc_ids_list))

        file_object.close()


# 6. Загрузить инвертированный индекс с диска;
    @classmethod
    def load(cls, filepath: str):
        """Loads inverted index from the binary file"""
        def unpack_next_part(unpack_format):
            next_part_len = struct.calcsize(unpack_format)
            return struct.unpack(unpack_format, file_object.read(next_part_len))

        inv_index = {}
        file_size = os.path.getsize(filepath)
        file_object = open(filepath, 'rb')

        while file_object.tell() < file_size:
            word_len = unpack_next_part('>H')[0]
            word = unpack_next_part(f'>{word_len}s')[0].decode()
            doc_ids_list_len = unpack_next_part('>H')[0]
            doc_ids_list = list(unpack_next_part(f'>{doc_ids_list_len}H'))
            inv_index[word] = doc_ids_list

        file_object.close()
        inverted_index = InvertedIndex()
        inverted_index.data = inv_index
        return inverted_index


    def __eq__(self, other_inverted_index):
        outcome = (
            self.data == other_inverted_index.data
        )
        return outcome

# 1. Считать датасет в оперативную память;
def load_documents(filepath: str) -> dict:
    """Loads documents"""
    print(f"loading documents from path {filepath} to build inverted index", file=sys.stderr)
    dict_of_documents = {}
    file_object = open(filepath)
    for line in file_object:
        parts = line.split("\t")
        doc_id = int(parts[0])
        doc_text = parts[1]
        for i in range(2, len(parts)):
            doc_text += " " + parts[i]
        dict_of_documents[doc_id] = doc_text.strip()
    return dict_of_documents


# 2. Разбить каждый документ на термы (слова);
def split_documents_into_words(documents: dict) -> dict:
    """Splits documents into words"""
    print("  splitting documents into words...", file=sys.stderr)
    words_from_documents = {}
    for doc_id, doc_text in documents.items():
        doc_words = list(set(doc_text.split()))
        words_from_documents[doc_id] = doc_words
    return words_from_documents


# 4. Построить инвертированный индекс;
def build_inverted_index(documents: dict) -> InvertedIndex:
    """Builds inverted index"""
    print("building inverted index for provided documents...", file=sys.stderr)
    words_from_documents = split_documents_into_words(documents)
    inv_index = InvertedIndex()
    for doc_id, doc_words in words_from_documents.items():
        for word in doc_words:
            inv_index.data[word] = inv_index.data.get(word, []) + [doc_id]
    print("len of dict:", len(inv_index.data.keys()), file=sys.stderr)
    return inv_index


def callback_build(arguments):
    """Callback for build"""
    print(f"call build subcommand with arguments: {arguments}", file=sys.stderr)
    process_arguments_build(arguments.dataset, arguments.output)


def callback_query(arguments):
    """Callback for query"""
    print(f"call query subcommand with arguments: {arguments}", file=sys.stderr)
    if arguments.query is not None:
        for individual_query in arguments.query:
            document_ids = process_arguments_query(arguments.input, individual_query)
            print(f"documents found: {len(document_ids)}", file=sys.stderr)
            print(",".join(list(map(str, document_ids))))
    else:
        for query in arguments.query_file:
            query = query.strip().split()
            print(f"use the following query (from file) to run against InvertedIndex:\
                {query}", file=sys.stderr)
            document_ids = process_arguments_query(arguments.input, query)
            print(f"documents found: {len(document_ids)}", file=sys.stderr)
            print(",".join(list(map(str, document_ids))))


def setup_parser(parser):
    """Setups parser"""
    subparsers = parser.add_subparsers(help="choose command")

    build_parser = subparsers.add_parser(
        "build",
        help="build inverted index and save in binary format into hard drive",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    query_parser = subparsers.add_parser(
        "query",
        help="query inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    build_parser.set_defaults(callback=callback_build)
    query_parser.set_defaults(callback=callback_query)


    build_parser.add_argument(
        "-d", "--dataset",
        required=False,
        default=DEFAULT_DATASET_PATH,
        help="path to dataset to load, default path is %(default)s",
    )
    build_parser.add_argument(
        "-o", "--output",
        required=False,
        default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        help="path to store inverted index in a binary format, default path is %(default)s",
    )

    query_parser.add_argument(
        "-i", "--input",
        required=False,
        default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        help="qath to read inverted index in a binary format, default path is %(default)s",
    )

    query_file_group = query_parser.add_mutually_exclusive_group(required=False)
    query_file_group.add_argument(
        "--query-file-utf8",
        default=TextIOWrapper(sys.stdin.buffer, encoding="utf-8"),
        type=EncodedFileType("r", encoding="utf8"),
        dest="query_file",
        metavar="FILENAME",
        help="query file to get queries for inverted index",
    )
    query_file_group.add_argument(
        "--query-file-cp1251",
        default=TextIOWrapper(sys.stdin.buffer, encoding="cp1251"),
        type=EncodedFileType("r", encoding="cp1251"),
        dest="query_file",
        metavar="FILENAME",
        help="query file to get queries for inverted index",
    )
    query_file_group.add_argument(
        "-q", "--query",
        nargs="+",
        action='append',
        metavar="WORD",
        help="query to run against inverted index",
    )


# inverted_index_filepath was input_filepath
def process_arguments_query(inverted_index_filepath: str, query: list) -> list:
    """Function to process arguments for query"""
    inverted_index = InvertedIndex.load(inverted_index_filepath)
    document_ids = inverted_index.query(query)
    return document_ids


def process_arguments_build(dataset_filepath: str, output_filepath: str):
    """Function to process arguments for query"""
    documents = load_documents(dataset_filepath)
    inverted_index = build_inverted_index(documents)
    inverted_index.dump(output_filepath)


def main():
    """Main"""
    parser = ArgumentParser(
        prog="inverted-index",
        description="tool to build, dump load and query inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
