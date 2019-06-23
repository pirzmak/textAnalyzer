from newsArticleModule.getarticleapi import get_data_from_news_api
from newsArticleModule.model import ArticleApiResponse
from stockMarketModule.getstockmarketapi import get_stock_prices_day
from datetime import datetime


def get_article_data(from_date, to_date, query):
    articles: [ArticleApiResponse] = get_data_from_news_api(from_date, to_date, query)
    print(articles)


print(get_stock_prices_day("AAPL", datetime(2019, 5, 8, 9, 30)))
print(get_stock_prices_day("AAPL", datetime(2019, 5, 8, 10, 30)))
print(get_stock_prices_day("AAPL", datetime(2019, 5, 8, 11, 30)))
print(get_stock_prices_day("AAPL", datetime(2019, 5, 8, 12, 30)))
