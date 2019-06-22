from newsapi import NewsApiClient
from .mymodel import ArticleApiResponse
import config
import urllib
from bs4 import BeautifulSoup

# APIKEY
API_KEY = config.config["NEWS_API_KEY"]


def get_data_from_news_api(from_date, to_date, query):
    news_api = NewsApiClient(api_key=API_KEY)

    response = news_api.get_everything(q=query,
                                       sources='bbc-news,the-verge',
                                       domains='bbc.co.uk,techcrunch.com',
                                       from_param=from_date,
                                       to=to_date,
                                       language='en',
                                       sort_by='relevancy',
                                       page_size=1,
                                       page=1)

    article_api_response = map(lambda j: ArticleApiResponse(j), response['articles'])
    full_content = map(lambda j: get_full_articles_content(j), article_api_response)
    return list(full_content)


def get_full_articles_content(article):
    with urllib.request.urlopen(article.url) as url:
        html = url.read()
        soup = BeautifulSoup(html)

        return parse_article(soup)


def parse_article(article):
    # kill all script and style elements
    for script in article(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = article.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    return ' '.join(chunk for chunk in chunks if chunk)


