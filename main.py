from newsArticleModule.getarticleapi import get_data_from_news_api
from newsArticleModule.model import ArticleApiResponse
from stockMarketModule.getstockmarketapi import get_stock_after_before_actual_price
from newsArticleModule.textanalizer import get_count_bags_of_word
from newsArticleModule.textanalizer import get_count_nouns_phrases
from newsArticleModule.textanalizer import get_count_named_entity
from dataBase.model import Record
from dataBase.mango_db import insert_many
from dataBase.mango_db import how_many_records
from config import dictionares
import config


BAGS_OF_WORDS = config.config['DB_collections_name_bags_of_words']
NAMES_ENTITIES = config.config['DB_collections_name_names_entities']
NOUNS = config.config['DB_collections_name_nouns']


def get_article_data(from_date, to_date, sign, query):
    mapped_bags_of_words = []
    mapped_names_entities = []
    mapped_nouns = []
    idx = 1
    articles: [ArticleApiResponse] = get_data_from_news_api(from_date, to_date, query, 100, idx)
    for a in articles:
        bags_of_word = get_count_bags_of_word(a.content)
        nouns = get_count_nouns_phrases(a.content)
        names_entities = get_count_named_entity(a.content)
        prices = get_stock_after_before_actual_price(sign, a.publishedAt)
        mapped_bags_of_words.append(Record(a.title, bags_of_word, a.publishedAt, prices))
        mapped_nouns.append(Record(a.title, nouns, a.publishedAt, prices))
        mapped_names_entities.append(Record(a.title, names_entities, a.publishedAt, prices))
    return mapped_bags_of_words, mapped_names_entities, mapped_nouns


def get_all_articles_from_dict(from_date, to_date, dict):
    for word in dict:
        bags_of_word, names_entities, nouns = get_article_data(from_date, to_date, dict[0], word)
        # insert_many(BAGS_OF_WORDS, bags_of_word)
        # insert_many(NAMES_ENTITIES, names_entities)
        # insert_many(NOUNS, nouns)
        print(bags_of_word)





dictionares.amazon_dict.extend(dictionares.technology_dict)
get_all_articles_from_dict('2019-06-03', '2019-06-03', dictionares.amazon_dict)
