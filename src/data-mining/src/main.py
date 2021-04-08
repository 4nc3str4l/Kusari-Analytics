import requests
import json
import time
import logging
import os

from lib.blockchain import Blockchain
from lib.sender import MessageSender

def main():
    blockchain = Blockchain(
        os.environ.get('SERVER_IP', None),
        os.environ.get('SERVER_PORT', None)
    )

    sender = MessageSender(host='rabbit', queues=('kusari', 'metrics'))
    
    blockchain.add_block_callback(lambda block: sender.send('kusari', {
        'type': 'nonce',
        'data': {
            'nonce': block['data']['hyperblock']['nonce']
        }
    }))
    
    blockchain.run()


if __name__ == "__main__":
    main()
