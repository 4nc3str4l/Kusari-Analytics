from .sender import MessageSender
from .blockchain import Blockchain

import time


def roll_list(lst: list, now: float):
    lst.append(now)

    while lst[0] < now - 60 * 60 * 24:
        lst.pop(0)


class Transactions(object):
    def __init__(self, blockchain: Blockchain):
        self.sender = MessageSender(host='rabbit', queues=('kusari', 'transactions'))

        self.rolling_24_blocks = []
        self.rolling_24_txs = []
        
        blockchain.add_block_callback(self.on_block)
        blockchain.add_after_block_callback(self.publish)
        blockchain.add_tx_callback(self.on_tx)

    def on_block(self, block):
        # TODO(gpascualg): Take block time instead of local?
        now = time.time()
        roll_list(self.rolling_24_blocks, now)
        
    def on_tx(self, tx):
        # TODO(gpascualg): Take transaction time instead of local?
        now = time.time()
        roll_list(self.rolling_24_txs, now)
        
    def publish(self, block):
        self.sender.send('transactions', {
            'type': 'after-block',
            'data': {
                'rolling_24_blocks': len(self.rolling_24_blocks),
                'rolling_24_txs': len(self.rolling_24_txs)
            }
        })
