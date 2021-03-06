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

        # Retrieve last nonce already
        self.last_nonce = Database().get_last_nonce()
        if not self.last_nonce:
            resp = self.get('v1.0/network/status/4294967295')
            self.last_nonce = resp['data']['status']['erd_highest_final_nonce']

    def add_block_callback(self, callback):
        self._on_block.append(callback)

    def add_after_block_callback(self, callback):
        self._after_block.append(callback)
    
    def add_tx_callback(self, callback):
        self._on_tx.append(callback)

    def get(self, path, retries=0):
        if retries >= 3:
            raise RuntimeError('Exceeded maximum retries')
        
        logger.debug(f'Querying {path}')
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

    def __get_block(self, nonce):
        return self.get(f'v1.0/hyperblock/by-nonce/{nonce}')

    def __get_tx(self, hash, sender):
        if sender != 'metachain':
            return self.get(f'v1.0/transaction/{hash}?sender={sender}&withResults=true')
        return self.get(f'v1.0/transaction/{hash}?withResults=true')

    def get_block_txs(self, nonce):
        resp = self.__get_block(nonce)
        for tx in resp['data']['hyperblock']['transactions']:
            tx = self.__get_tx(tx['hash'], tx['sender'])
            yield tx

    def __process(self, tx):
        resp = self.__get_tx(tx['hash'], tx['sender'])
        for callback in self._on_tx:
            callback(resp)

    def __fetch(self, nonce):
        logger.info('Fetching %d', nonce)

        # Get block, call callbacks
        resp = self.__get_block(nonce)
        for callback in self._on_block:
            callback(resp)

        for tx in resp['data']['hyperblock']['transactions']:
            logger.debug('\tHas tx %s', tx['hash'])
            self.__process(tx)

        for callback in self._after_block:
            callback(resp)

    def run(self):
        while True:
            resp = self.get('v1.0/network/status/4294967295')
            nonce = resp['data']['status']['erd_highest_final_nonce']

            for currentNonce in range(self.last_nonce + 1, nonce + 1):
                self.__fetch(currentNonce)
            
            self.last_nonce = nonce
            Database().save_last_nonce(nonce)
            time.sleep(5)
        