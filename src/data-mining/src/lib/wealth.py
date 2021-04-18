from .blockchain import Blockchain
from .database import Database

import bisect 


class Address(object):
    def __init__(self, address, balance):
        self.address = address
        self.balance = balance


class Wealth(object):
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.last_nonce = Database().get_last_wealth_nonce()

        # Add tx callback
        blockchain.add_tx_callback(self.on_tx)

        # Top-1000 addresses
        self.top_addresses = []
        self.cutout = 0


    def load_missing(self, current_nonce):
        previous_nonce, self.last_nonce = self.last_nonce, current_nonce
        for nonce in range(previous_nonce, self.last_nonce):
            for tx in self.blockchain.get_block_txs(nonce):
                self.on_tx(tx)

    def on_tx(self, tx):
        tx_data = tx['data']['transaction']
        if tx_data['type'] != 'normal':
            return
        
        updated_receiver = Database().increase_address_balance(tx_data['receiver'], tx_data['amount'])
        updated_sender = Database().decrease_address_balance(tx_data['sender'], tx_data['amount'])

        # Has the sender fallen off the top-list?
        if self.top_addresses[-1].address == updated_sender['_id']:

        self.top_addresses.