class Record:
    def __init__(self, title, content, date, price):
        self.title = title
        self.text_vector = content
        self.date = date
        self.before_price = price['before']
        self.actual_price = price['actual']
        self.after_price = price['after']

    def to_record(self):
        return {
            "title": self.title,
            "text_vector": self.text_vector,
            "date": self.date,
            "before_price": self.before_price,
            "actual_price": self.actual_price,
            "after_price": self.after_price
        }
