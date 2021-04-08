from .config import logger
from .database import Database

import requests
import time


class Blockchain(object):
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self._on_block = []
        self._after_block = []
        self._on_tx = []

    def add_block_callback(self, callback):
        self._on_block.append(callback)

    def add_after_block_callback(self, callback):
        self._after_block.append(callback)
    
    def add_tx_callback(self, callback):
        self._on_tx.append(callback)

    def get(self, path, retries=0):
        if retries >= 3:
            raise RuntimeError('Exceeded maximum retries')
        
        try:
            url = f'http://{self.server_ip}:{self.server_port}/{path}'
            return requests.get(url).json()
        except requests.exceptions.Timeout:
            return self.get(path, retries + 1)
        except requests.exceptions.TooManyRedirects:
            return self.get(path, retries + 1)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)

    def process(self, tx):
        resp = self.get(f'v1.0/transaction/{tx["hash"]}?sender={tx["sender"]}&withResults=true')
        for callback in self._on_tx:
            callback(resp)

    def fetch(self, nonce):
        logger.info('Fetching %d', nonce)

        # Get block, call callbacks
        resp = self.get(f'v1.0/hyperblock/by-nonce/{nonce}')
        for callback in self._on_block:
            callback(resp)

        for tx in resp['data']['hyperblock']['transactions']:
            logger.debug('\tHas tx %s', tx['hash'])
            self.process(tx)

        for callback in self._after_block:
            callback(resp)

    def run(self):
        lastNonce = Database().get_last_nonce()
    
        if not lastNonce:
            resp = self.get('v1.0/network/status/4294967295')
            lastNonce = resp['data']['status']['erd_highest_final_nonce']
    

        while True:
            resp = self.get('v1.0/network/status/4294967295')
            nonce = resp['data']['status']['erd_highest_final_nonce']

            for currentNonce in range(lastNonce + 1, nonce + 1):
                self.fetch(currentNonce)
            
            lastNonce = nonce
            Database().save_last_nonce(nonce)
            time.sleep(5)
        