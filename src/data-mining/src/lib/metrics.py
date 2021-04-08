from .sender import MessageSender
from .blockchain import Blockchain

import time


class Metrics(object):
    def __init__(self, blockchain: Blockchain):
        self.sender = MessageSender(host='rabbit', queues=('kusari', 'metrics'))

        self.rolling_24_blocks = []
        self.rolling_24_txs = []
        
        blockchain.add_block_callback(self.on_block)
        blockchain.add_after_block_callback(self.publish)
        blockchain.add_tx_callback(self.on_tx)

    def on_block(self, block):
        # TODO(gpascualg): Take block time instead of local?
        now = time.time()
        self.rolling_24_blocks.append(now)

        while self.rolling_24_blocks[0] < now - 60 * 60 * 24:
            self.rolling_24_blocks.pop(0)
        
    def on_tx(self, tx):
        # TODO(gpascualg): Take transaction time instead of local?
        now = time.time()
        self.rolling_24_txs.append(now)

        while self.rolling_24_txs[0] < now - 60 * 60 * 24:
            self.rolling_24_txs.pop(0)
        
    def publish(self, block):
        self.sender.send('metrics', {
            'type': 'after-block',
            'data': {
                'rolling_24_blocks': len(self.rolling_24_blocks),
                'rolling_24_txs': len(self.rolling_24_txs)
            }
        })
