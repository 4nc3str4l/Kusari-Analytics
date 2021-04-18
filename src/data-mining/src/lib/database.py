from .singleton import ThreadedSingleton

import pymongo


class Database(object, metaclass=ThreadedSingleton):
    def __init__(self):
        self.client = pymongo.MongoClient('mongo-data-mining')
        self.db = self.client.kusari

    def get_last_nonce(self, default=None):
        obj = self.db.config.find_one({
            '_id': 'nonce'
        })
        return default if obj is None else obj['value']

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
        return default if obj is None else obj['value']

    def save_last_wealth_nonce(self, nonce):
        self.db.config.update_one({'_id': 'wealth_nonce'}, {
            '$set': {
                'value': nonce
            }
        }, upsert=True)

    def increase_address_balance(self, address, amount):
        return self.db.addresses.find_one_and_update({'_id': address}, {
            '$inc': {
                'balance': amount
            }
        })

    def decrease_address_balance(self, address, amount):
        return self.db.addresses.update_one({'_id': address}, {
            '$inc': {
                'balance': -amount
            }
        })

    def get_top_holders_from_position(self, position):
        cursor = self.db.addresses.find({
            'balance': {
                '$gt': 0
            }
        }).sort({'balance': pymongo.DESCENDING}).skip(position - 1)
        return cursor

    def get_top_holder_at_position(self, position):
        cursor = self.get_top_holders_from_position(position).limit(1)
        return next(cursor, None)

    def get_top_holders(self, maximum):
        return self.get_top_holders_from_position(1).limit(maximum)
