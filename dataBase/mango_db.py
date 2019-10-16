import pymongo
from .model import Record
from config.config import config

myclient = pymongo.MongoClient(config["DB_host"])
mydb = myclient[config["DB_name"]]


def insert(name: str, record: Record):
    mycol = mydb[name]
    mycol.insert_one(record.to_record())


def insert_many(name: str, records: [Record]):
    mycol = mydb[name]
    if records:
        mycol.insert_many(list(map(lambda r: r.to_record(), records)))


def select_all(column: str):
    mycol = mydb[column]
    return mycol.find()


def select_by_tag(column: str, tag: str):
    mycol = mydb[column]
    return mycol.find({'tag': tag}, no_cursor_timeout=True)


def select(column: str, query):
    mycol = mydb[column]
    return mycol.find(query, no_cursor_timeout=True)


def update(column: str, query, value):
    mycol = mydb[column]
    return mycol.update_one(query, value)


def how_many_records(name: str):
    print(mydb[name].count())

def clear(name: str):
    mycol = mydb[name]
    mycol.remove()

