# Kusari (鎖) -Analytics
A platform to create secure and open analitycs for smart contracts powered by the Elrond Blockchain.

The api for the smart contract should be something simple:

```
Kusary.LogAction("asset_allocated", {quantity: "10",  ticker: "usdt", ts: "10001"} );
```
(I'm not sure of the syntax as I don't know yet how to code Elrond Smart Contracts)

Then we should be able to display these arrays of data offering different options.

Then on the Visualization Pannel we need to be able to do something like:

```
// Get all the data for the smart contract
const smartContractData = new Kusary.SmartContractData("addr");

// Obtain all the asset_allocation actions
const assetAllocation = smartContractData.GetAll("asset_allocation").OrderBy("ts").Asc();

// Get only the ones that the key ticker is usdt
usdt_data = assetAllocation.filter("ticker", "usdt");

// Create a label that shows the total ammount of USDT allocated:
const view = Kusary.View.CreateText("Total USDT asset allocation %d USDT", Sum(usdt_data["quantity"]));

```

This data visualization should be able to be encoded on the url of the page in order to be shader.
