#!/usr/bin/env python3
"""Popularity index module"""
import json
import logging
import logging.config
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from re import findall as re_findall

from lxml import etree
import yaml




APPLICATION_NAME = "popularity_index"
DEFAULT_LOGGING_CONFIG_PATH = "logging.conf.yml"

#POSTS_FPATH = "stackoverflow_posts_sample_short.xml"
#STOP_WORDS_FPATH = "stop_words_en_koi8-r.txt"
#QUERIES_FPATH = "queries.csv"


logger = logging.getLogger(APPLICATION_NAME)


class PopularityIndex:
    """Popularity index class"""
    def __init__(self):
        self.data = {}

    def query(self, start_year: int, end_year: int, top_n: int) -> dict:
        """Prints analytics results"""
        logger.debug("got query \"%s,%s,%s\"", start_year, end_year, top_n)
        actual_words = {}
        for year in range(start_year, end_year + 1):
            current_dict_for_year = self.data.get(year, {})
            for word in current_dict_for_year.keys():
                actual_words[word] = actual_words.get(word, 0) + current_dict_for_year[word]
        actual_words_list = [[word, score] for word, score in actual_words.items()]
        actual_words_list = sorted(
            actual_words_list, key=lambda word_tuple: word_tuple[0], reverse=False)
        actual_words_list = sorted(
            actual_words_list, key=lambda word_tuple: word_tuple[1], reverse=True)
        words_found = len(actual_words_list)
        if words_found < top_n:
            logger.warning("not enough data to answer, found %s words out of %s for period \"%s,%s\"", words_found, top_n, start_year, end_year)
        actual_words_list = actual_words_list[:top_n]
        response = {"start": start_year, "end": end_year, "top": actual_words_list}
        return response


    def queries_from_file(self, filepath: str):
        """Function to call query one by one from file"""
        fin = open(filepath)
        for line in fin:
            start_year, end_year, top_n = list(map(int, line.split(",")))
            response = self.query(start_year, end_year, top_n)
            response_json = json.dumps(response)
            print(response_json)
        fin.close()
        logger.info("finish processing queries")


def get_stop_words(filepath: str) -> set:
    """Returns set of stop words"""
    fin = open(filepath, encoding="koi8-r")
    set_of_stop_words = set()
    for word in fin:
        set_of_stop_words.add(word.strip().lower())
    fin.close()
    return set_of_stop_words


def get_data(filepath: str, stop_words: set = None) -> PopularityIndex:
    """Loads posts and builds popularity index"""
    if stop_words is None:
        stop_words = set()
    error_exists = False
    pop_index_dict = {}
    fin = open(filepath)
    for xml_line in fin:
        try:
            root = etree.fromstring(xml_line)
            post_type = root.get("PostTypeId")
            if post_type == "1":
                title = root.get("Title")
                creation_year = int(root.get("CreationDate")[:4])
                score = int(root.get("Score"))

                words = set(re_findall("\\w+", title.lower()))
                for word in words:
                    if word not in stop_words:
                        current_dict_for_year = pop_index_dict.get(creation_year, {})
                        current_score = current_dict_for_year.get(word, 0)
                        updated_score = current_score + score
                        current_dict_for_year[word] = updated_score
                        pop_index_dict[creation_year] = current_dict_for_year
        except:
            error_exists = True

    pop_index = PopularityIndex()
    pop_index.data = pop_index_dict
    fin.close()
    #print(json.dumps(pop_index_dict, indent=2, sort_keys=True))
    logger.info("process XML dataset, ready to serve queries")
    return pop_index


def callback_analytics(arguments):
    """Callback for analytics"""
    process_arguments_analytics(arguments.questions, arguments.stop_words, arguments.queries)


def setup_parser(parser):
    """Setups parser"""
    parser.set_defaults(callback=callback_analytics)

    parser.add_argument(
        "--questions",
        required=True,
        default=None,
        help="path to dataset with stackoverflow posts in xml format, default path is %(default)s",
        metavar="FPATH",
    )
    parser.add_argument(
        "--stop-words",
        required=True,
        default=None,
        help="path to file with stop-words in txt format (koi8-r), default path is %(default)s",
        metavar="FPATH",
    )
    parser.add_argument(
        "--queries",
        required=True,
        default=None,
        help="path to queries in csv format, default path is %(default)s",
        metavar="FPATH",
    )


def process_arguments_analytics(
        questions_filepath: str, stop_words_filepath: str, queries_filepath: str
    ):
    """Function to process arguments"""
    stop_words = get_stop_words(stop_words_filepath)
    pop_index = get_data(questions_filepath, stop_words)
    pop_index.queries_from_file(queries_filepath)


def setup_logging():
    """Setups logging configurations"""
    with open(DEFAULT_LOGGING_CONFIG_PATH) as config_fin:
        logging.config.dictConfig(yaml.safe_load(config_fin))


def main():
    """Main"""
    setup_logging()
    parser = ArgumentParser(
        prog="popularity-index",
        description="tool analyze stackoverflow posts",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)


if __name__ == "__main__":
    main()
