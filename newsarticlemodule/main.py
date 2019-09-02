from newsarticlemodule.getarticleapi import get_data_from_news_api
from newsarticlemodule.model import ArticleApiResponse
from newsarticlemodule.textanalizer import get_count_bags_of_word
from newsarticlemodule.textanalizer import get_count_nouns_phrases
from newsarticlemodule.textanalizer import get_count_named_entity
from dataBase.model import Record
from dataBase.mango_db import insert_many
import config

BAGS_OF_WORDS = config.config['DB_collections_name_bags_of_words']
NAMES_ENTITIES = config.config['DB_collections_name_names_entities']
NOUNS = config.config['DB_collections_name_nouns']


def get_article_data(from_date, to_date, query, tag):
    mapped_bags_of_words = []
    mapped_names_entities = []
    mapped_nouns = []
    idx = 1
    articles: [ArticleApiResponse] = get_data_from_news_api(from_date, to_date, query, 100, idx)
    for a in articles:
        bags_of_word = get_count_bags_of_word(a.content)
        nouns = get_count_nouns_phrases(a.content)
        names_entities = get_count_named_entity(a.content)
        mapped_bags_of_words.append(Record(tag, a.title, bags_of_word, a.publishedAt))
        mapped_nouns.append(Record(tag, a.title, nouns, a.publishedAt))
        mapped_names_entities.append(Record(tag, a.title, names_entities, a.publishedAt))
    return mapped_bags_of_words, mapped_names_entities, mapped_nouns


def get_all_articles_from_dict(from_date, to_date, dict, tag):
    for word in dict:
        bags_of_word, names_entities, nouns = get_article_data(from_date, to_date, word, tag)
        insert_many(BAGS_OF_WORDS, bags_of_word)
        insert_many(NAMES_ENTITIES, names_entities)
        insert_many(NOUNS, nouns)
        print(len(bags_of_word))
    print(len(dict))