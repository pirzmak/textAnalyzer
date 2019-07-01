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


def how_many_records(name: str):
    print(mydb[name].count())
