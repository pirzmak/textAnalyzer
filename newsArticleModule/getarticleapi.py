from newsapi import NewsApiClient
from mymodel import ArticleApiResponse
import urllib
from bs4 import BeautifulSoup

# APIKEY
api_key = '72e7bba0059148e29591164a6be2b18b'


def get_data_from_news_api(from_date, to_date, query):
    newsapi = NewsApiClient(api_key=api_key)

    response = newsapi.get_everything(q=query,
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param=from_date,
                                      to=to_date,
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)

    article_api_response = map(lambda j: ArticleApiResponse(j), response['articles'])
    full_content = map(lambda j: get_full_articles_content(j), article_api_response)
    return list(full_content)


def get_full_articles_content(article):
    with urllib.request.urlopen(article.url) as url:
        html = url.read()
        soup = BeautifulSoup(html)

        return parse_article(soup)


def parse_article(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    return '\n'.join(chunk for chunk in chunks if chunk)


def test():
    text = get_data_from_news_api('2019-05-17', '2019-06-17', 'it')
    print(text)


test()
