from .singleton import ThreadedSingleton

from pymongo import MongoClient


class Database(object, metaclass=ThreadedSingleton):
    def __init__(self):
        self.client = MongoClient('mongo-data-mining')
        self.db = self.client.kusari

    def get_last_nonce(self, default=None):
        obj = self.db.config.find_one({
            '_id': 'nonce'
        })
        return obj['value'] or default

    def save_last_nonce(self, nonce):
        self.db.config.update_one({'_id': 'none'}, {
            '$set': {
                'value': nonce
            }
        }, upsert=True)

    def get_last_wealth_nonce(self, default=0):
        obj = self.db.config.find_one({
            '_id': 'wealth_nonce'
        })
        return obj['value'] or default

    def save_last_wealth_nonce(self, nonce):
        self.db.config.update_one({'_id': 'wealth_nonce'}, {
            '$set': {
                'value': nonce
            }
        }, upsert=True)

