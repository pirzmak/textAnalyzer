import pymongo
from model import Record


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["textAnalize"]


def insert(name: str, record: Record):
    mycol = mydb[name]
    mycol.insert_one(record.toRecord())


def insert_many(name: str, records: [Record]):
    mycol = mydb[name]
    mycol.insert_one(list(map(lambda r: r.toRecord(), records)))