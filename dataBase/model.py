class Record:
    def __init__(self, tag, title, content, date):
        self.tag = tag
        self.title = title
        self.text_vector = content
        self.date = date

    def to_record(self):
        return {
            "tag": self.tag,
            "title": self.title,
            "text_vector": self.text_vector,
            "date": self.date
        }
