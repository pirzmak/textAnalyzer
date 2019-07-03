from newsapi import NewsApiClient
from .model import ArticleApiResponse
import config
import urllib
from bs4 import BeautifulSoup

# APIKEY
API_KEY = config.config["NEWS_API_KEY"]


def get_data_from_news_api(from_date, to_date, query, page_size, page):
    news_api = NewsApiClient(api_key=API_KEY)

    response = news_api.get_everything(q=query,
                                       sources='bbc-news',
                                       domains='bbc.co.uk,techcrunch.com',
                                       from_param=from_date,
                                       to=to_date,
                                       language='en',
                                       sort_by='relevancy',
                                       page_size=page_size,
                                       page=page)

    article_api_response = []
    for a in response['articles']:
        try:
            article = ArticleApiResponse(a)
            article.content = get_full_articles_content(article)
            article_api_response.append(article)
        except urllib.error.HTTPError:
            print("Can't get article")
    return article_api_response


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


