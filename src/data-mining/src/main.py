import requests
import json
import time
import logging
import os

from lib.blockchain import Blockchain
from lib.transactions import Transactions
from lib.sender import MessageSender, DECL_QUEUES
from lib.wealth import Wealth


def main():
    # Create blockchain listener
    blockchain = Blockchain(
        os.environ.get('SERVER_IP', None),
        os.environ.get('SERVER_PORT', None)
    )

    # Create a queue and register a block callback
    sender = MessageSender(host='rabbit', queues=DECL_QUEUES)
    blockchain.add_block_callback(lambda block: sender.send('kusari', {
        'type': 'nonce',
        'data': {
            'nonce': block['data']['hyperblock']['nonce']
        }
    }))

    # Create the transactions service
    Transactions(blockchain)

    # Create wealth checker service
    Wealth(blockchain, blockchain.last_nonce)
    
    # Indefinitely block
    blockchain.run()


if __name__ == "__main__":
    main()
