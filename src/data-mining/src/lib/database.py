from .singleton import ThreadedSingleton

from pymongo import MongoClient


class Database(object, meta=ThreadedSingleton):
    def __init__(self):
        self.client = MongoClient('mongo-data-mining')
        self.db = self.client.kusari

    def get_last_nonce(self, default=None):
        nonce = self.db.config.find_one({
            '_id': 'nonce'
        })
        return nonce or default

    def save_last_nonce(self, nonce):
        self.db.config.update_one({'_id': 'none'}, {
            '$set': {
                'value': nonce
            }
        })
    