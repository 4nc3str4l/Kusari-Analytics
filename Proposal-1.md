# Proposal-1

Smart contract does not hold much logic, it serves as an endpoint we can watch. A python/something else script listens for calls on it, and processes in RAM the necessary data.

## Advantages

1. Keeps contract cost low, as it won't do much
2. There is little storage involved, we would only need a simple DB in case we have to restart or something goes wrong

## Disadvantages
1. Low cost means low fees, which means low income

2. Actively listening the blockchain means problems in case of downtime

    * We would have to parse all blocks from the time it went down, which can be quite a lot

    * We can't use any data that is stored in the smart contract, as by the time we are up, it might have changed

## Overview

The contract would server as an API

* registerVisit(endpoint, visitor)

    * Trigger event, onVisitor(endpoint, visitor)

    * Catch event in python and process it

* addBalance(who, amount, token)

    * Trigger event, addedBalance(who, amount, token)

We would just need to reactively maintain centralized metrics based on the information from the events.



# Implementation details

## Rest endpoints

### Get latest block nonce
`/v1.0/network/status/4294967295`

### Get the latest block
`/v1.0/hyperblock/by-nonce/*:nonce*`

### Details of a transaction
`/v1.0/transaction/*:txHash*?withResults=true`
> withResults outputs also smart-contrac related events

`/v1.0/transaction/:*txHash*?sender=*:senderAddress*&withResults=true`
> Having the sender speeds up the process, as only one shard observer will be used


## Sample pseudocode
```python
def process(tx):
    results = get(f'/v1.0/transaction/{tx["hash"]}?sender={tx["sender"]}&withResults=true')
    
    # Parse results, look for events

def fetch(nonce):
    block = get(f'/v1.0/hyperblock/by-nonce/{nonce}')
    for tx in block['transactions']:
        if tx['receiver'] == OUR_SMART_CONTRACT_ADDRESS:
            process(tx)

def main():
    lastNonce = db.getLastNonce()

    while True:
        nonce = get(f'/v1.0/network/status/4294967295')
        for currentNonce in range(lastNonce, nonce):
            fetch(currentNonce)
        
        lastNonce = nonce
        db.saveLastNonce(nonce)
```
