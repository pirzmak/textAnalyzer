import pymongo
from .model import Record
from config.config import config

myclient = pymongo.MongoClient(config["DB_host"])
mydb = myclient[config["DB_name"]]


def insert(name: str, record: Record):
    mycol = mydb[name]
    mycol.insert_one(record.toRecord())


def insert_many(name: str, records: [Record]):
    mycol = mydb[name]
    mycol.insert_one(list(map(lambda r: r.toRecord(), records)))