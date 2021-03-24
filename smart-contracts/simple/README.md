# Interaction

## On local devnet

Deploy & interact with contract:

```
python3 ./interaction/playground.py --pem=./testnet/wallets/users/alice.pem --proxy=http://localhost:7950
```

Interact with existing contract:

```
python3 ./interaction/playground.py --pem=./testnet/wallets/users/alice.pem --proxy=http://localhost:7950 --contract=erd1...
```

## On devnet

Deploy & interact with contract:

```
python3 ./interaction/playground.py --pem=my.pem --proxy=https://devnet-gateway.elrond.com
```

Interact with existing contract:

```
python3 ./interaction/playground.py --pem=my.pem --proxy=https://devnet-gateway.elrond.com --contract=erd1...
```

## Deployed Smart Contracts on devnet:

https://devnet-explorer.elrond.com/accounts/erd1qqqqqqqqqqqqqpgq3zr2c448vndltl907gu37tmpvjzu50rcdf5sc95433
