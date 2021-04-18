from .sender import MessageSender
from .blockchain import Blockchain

from typing import Union
import time


ROLL_1H  = 60 * 60
ROLL_24H = ROLL_1H * 24


def roll_list(lst: list, now: Union[float, None], period):
    if now:
        lst.append(now)

    while lst and lst[0] < now - period:
        lst.pop(0)


class Transactions(object):
    def __init__(self, blockchain: Blockchain):
        self.sender = MessageSender(host='rabbit', queues=('kusari', 'transactions'))

        self.rolling_1_blocks = []
        self.rolling_1_non_empty_blocks = []
        self.rolling_1_txs = []
        self.rolling_1_txs_by_type = {}

        self.rolling_24_blocks = []
        self.rolling_24_non_empty_blocks = []
        self.rolling_24_txs = []
        self.rolling_24_txs_by_type = {}
        
        blockchain.add_block_callback(self.on_block)
        blockchain.add_after_block_callback(self.publish)
        blockchain.add_tx_callback(self.on_tx)

    def on_block(self, block):
        # TODO(gpascualg): Take block time instead of local?
        now = time.time()
        roll_list(self.rolling_24_blocks, now, ROLL_24H)
        roll_list(self.rolling_1_blocks, now, ROLL_1H)

        # If there are no transactions in the block, set
        #   now to None, which will only roll the list but
        #   not at any entry
        if not block['data']['hyperblock']['transactions']:
            now = None
        
        roll_list(self.rolling_24_non_empty_blocks, now, ROLL_24H)
        roll_list(self.rolling_1_non_empty_blocks, now, ROLL_1H)
        
    def on_tx(self, tx):
        # TODO(gpascualg): Take transaction time instead of local?
        now = time.time()
        roll_list(self.rolling_24_txs, now, ROLL_24H)
        roll_list(self.rolling_1_txs, now, ROLL_1H)

        # TODO(gpascualg): Which TX types do we have? [normal, ?]
        tx_type = tx['data']['transaction']['type']
        
        if tx_type not in self.rolling_24_txs_by_type:
            self.rolling_24_txs_by_type[tx_type] = []
        
        if tx_type not in self.rolling_1_txs_by_type:
            self.rolling_1_txs_by_type[tx_type] = []

        roll_list(self.rolling_24_txs_by_type[tx_type], now, ROLL_24H)
        roll_list(self.rolling_1_txs_by_type[tx_type], now, ROLL_1H)
        
    def publish(self, block):
        self.sender.send('transactions', {
            'type': 'after-block',
            'data': {
                'rolling_24h' : {
                    'blocks': len(self.rolling_24_blocks),
                    'non_empty_blocks': len(self.rolling_24_non_empty_blocks),
                    'txs': len(self.rolling_24_txs),
                    'txs_by_type': {
                        tx_type: len(lst) for tx_type, lst in self.rolling_24_txs_by_type.items()
                    }
                },
                'rolling_1h' : {
                    'blocks': len(self.rolling_1_blocks),
                    'non_empty_blocks': len(self.rolling_1_non_empty_blocks),
                    'txs': len(self.rolling_1_txs),
                    'txs_by_type': {
                        tx_type: len(lst) for tx_type, lst in self.rolling_1_txs_by_type.items()
                    }
                }
            }
        })
