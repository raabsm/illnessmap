from pymongo import MongoClient


class MongoConnection:

    def __init__(self, db, uri):
        self.client = MongoClient(uri)
        self.db = self.client[db]

    def return_collection(self, col):
        return self.db[col]
