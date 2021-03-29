import requests
import json
import time
import logging


logger = logging.getLogger("Kusari")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


CONFIG = {
    'server_ip': None,
    'server_port': None,
    'smart_contract_address': None
}

def get(path):
    url = f'http://{CONFIG["server_ip"]}:{CONFIG["server_port"]}/{path}'
    return requests.get(url).json()


def process(tx):
    logger.info('Processing %s', tx)
    resp = get(f'v1.0/transaction/{tx["hash"]}?sender={tx["sender"]}&withResults=true')
    
    # Parse results, look for events

def fetch(nonce):
    logger.info('Fetching %d', nonce)

    resp = get(f'v1.0/hyperblock/by-nonce/{nonce}')
    for tx in resp['data']['hyperblock']['transactions']:
        logger.debug('\tHas tx %s', tx['hash'])
        if tx['receiver'] == CONFIG['smart_contract_address']:
            process(tx)


def main():
    # Load config
    try:
        with open('config.json') as fp:
            for k, v in json.load(fp).items():
                CONFIG[k] = v
    except IOError:
        logger.critical('Config file \'config.json\' not found, it is not uploaded to git')
    except json.JSONDecodeError as e:
        logger.critical('Config file \'config.json\' is not a valid json file')
        raise e

    lastNonce = None #db.getLastNonce()
    if not lastNonce:
        resp = get('v1.0/network/status/4294967295')
        lastNonce = resp['data']['status']['erd_highest_final_nonce']
    

    while True:
        resp = get('v1.0/network/status/4294967295')
        nonce = resp['data']['status']['erd_highest_final_nonce']

        for currentNonce in range(lastNonce + 1, nonce + 1):
            fetch(currentNonce)
        
        lastNonce = nonce
        time.sleep(5)


if __name__ == "__main__":
    main()