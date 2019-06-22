from newsArticleModule.getarticleapi import get_data_from_news_api
from newsArticleModule.mymodel import ArticleApiResponse


def get_article_data(from_date, to_date, query):
    articles: [ArticleApiResponse] = get_data_from_news_api(from_date, to_date, query)
    print(articles)


get_article_data("2019-05-20", "2019-05-21", "it")
