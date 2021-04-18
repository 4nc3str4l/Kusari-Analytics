from .blockchain import Blockchain
from .database import Database


class Wealth(object):
    def __init__(self, blockchain: Blockchain):
        self.blockchain = blockchain
        self.last_nonce = Database().get_last_wealth_nonce()

        # Add tx callback
        blockchain.add_tx_callback(self.on_tx)
        

    def load_missing(self, current_nonce):
        previous_nonce, self.last_nonce = self.last_nonce, current_nonce
        for nonce in range(previous_nonce, self.last_nonce):
            for tx in self.blockchain.get_block_txs(nonce):
                self.on_tx(tx)

    def on_tx(self, tx):
        if tx['data']['transaction']['type'] != 'normal':
            return
        
        