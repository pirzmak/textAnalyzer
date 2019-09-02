import json
import os, ssl

with open("config/config.conf") as json_file:
    config = json.load(json_file)

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context


class TRENDS:
    BIG_DECREASE = 0
    DECREASE = 1
    NO_CHANGE = 2
    INCREASE = 3
    BIG_INCREASE = 4

    def get_trends(value):
        if value == TRENDS.BIG_DECREASE:
            return TRENDS.BIG_DECREASE
        if value == TRENDS.DECREASE:
            return TRENDS.DECREASE
        if value == TRENDS.NO_CHANGE:
            return TRENDS.NO_CHANGE
        if value == TRENDS.INCREASE:
            return TRENDS.INCREASE
        if value == TRENDS.BIG_INCREASE:
            return TRENDS.BIG_INCREASE


class DBNAMES:
    BAGS_OF_WORDS = config['DB_collections_name_bags_of_words']
    NAMES_ENTITIES = config['DB_collections_name_names_entities']
    NOUNS = config['DB_collections_name_nouns']


def resources_path(path):
    return config['resources_path'] + path
