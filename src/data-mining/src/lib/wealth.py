from .blockchain import Blockchain
from .config import logger
from .database import Database
from .sender import MessageSender, DECL_QUEUES

import bisect 
import threading


class Holder(object):
    def __init__(self, address, balance):
        self.address = address
        self.balance = balance


class Wealth(object):
    def __init__(self, blockchain: Blockchain, blockchain_last_nonce):
        self.blockchain = blockchain
        self.sender = MessageSender(host='rabbit', queues=DECL_QUEUES)
        self.last_nonce = Database().get_last_wealth_nonce()

        # Top-1000 addresses
        self.max_top_addresses = 1000
        self.top_addresses = []
        self.cutout = 0

        # Distribution update settings
        self.updating_missing = False
        self.block_has_changes = False

        # Add callbacks
        blockchain.add_block_callback(self.on_block)
        blockchain.add_after_block_callback(self.after_block)
        blockchain.add_tx_callback(self.on_tx)

        # Start loading missing data
        self.updating_thread = threading.Thread(target=self.__load_missing, args=(blockchain_last_nonce,))
        self.updating_thread.start()

    def __load_missing(self, current_nonce):
        self.updating_missing = True
            
        logger.debug(f'Load missing from {self.last_nonce} to {current_nonce}')

        previous_nonce, self.last_nonce = self.last_nonce, current_nonce
        for nonce in range(previous_nonce, self.last_nonce):
            logger.debug(f'Load missing wealth from block {nonce}')
            for tx in self.blockchain.get_block_txs(nonce):
                self.on_tx(tx) # Batch update first, no dist updates

        # Save nonce to DB
        Database().save_last_wealth_nonce(self.last_nonce)
        self.updating_missing = False

    def on_block(self, block):
        self.block_has_changes = False

    def after_block(self, block):
        # Save nonce
        Database().save_last_wealth_nonce(block['data']['hyperblock']['nonce'])

        # Check if there had been changes and we are not yet updating
        if self.updating_missing or not self.block_has_changes:
            return

        logger.debug(f'Sending rich-list changes')
        for position, data in enumerate(Database().get_top_holders(self.max_top_addresses)):
            # Check if we have this top-holder already
            if position < len(self.top_addresses):
                holder = self.top_addresses[position]

                # Has it changed at all?
                if holder.address == data['_id'] and holder.balance == data['balance']:
                    continue

                # Update holder and send to frontend
                holder.address = data['_id']
                holder.balance = data['balance']

                self.sender.send('wealth', {
                    'type': 'change',
                    'data': {
                        'position': position + 1,
                        'address': holder.address,
                        'balance': holder.balance
                    }
                })

            else:
                # It's a new entry, create it and send
                holder = Holder(data['_id'], data['balance'])
                self.top_addresses.append(holder)

                self.sender.send('wealth', {
                    'type': 'change',
                    'data': {
                        'position': position + 1,
                        'address': holder.address,
                        'balance': holder.balance
                    }
                })

            # Debug output
            logger.debug(f'[{position:04}] {holder.address}: {holder.balance}')

    def on_tx(self, tx):
        tx_data = tx['data']['transaction']
        
        # Normal transactions are value changes
        if tx_data['type'] == 'normal':
            # Set changes
            self.block_has_changes = True

            # Update DB
            value = int(tx_data['value'])
            updated_receiver = Database().increase_address_balance(tx_data['receiver'], value)
            updated_sender = Database().decrease_address_balance(tx_data['sender'], value)

        # Rewards are simple increases
        elif tx_data['type'] == 'reward':
            # Set changes
            self.block_has_changes = True

            # Update DB
            value = int(tx_data['value'])
            updated_receiver = Database().increase_address_balance(tx_data['receiver'], value)
    