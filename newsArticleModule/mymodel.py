from dateutil import parser


class ArticleApiResponse:
    def __init__(self, json):
        self.title = json['title']
        self.url = json['url']
        self.publishedAt = parser.parse(json['publishedAt'])
        self.content = ""
