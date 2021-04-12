package main

import (
"encoding/json"
"log"
"net/http"
)

type TransactionsMessage struct {
	Type string `json:"type"`
	Data TransactionsData `json:"data"`
}

type TransactionsData struct {
	Blocks uint64 `json:"rolling_24_blocks"`
	Transactions uint64 `json:"rolling_24_txs"`
}

func UpdateTransactions(chTransactions chan []byte) {
	transactionsListener.initialize()
	var f TransactionsMessage
	for {
		msg := <- chTransactions
		json.Unmarshal(msg, &f)
		transactionsListener.listenersMux.RLock()
		for ws, _ := range transactionsListener.listeners {
			_ = ws.WriteJSON(f.Data)
		}
		transactionsListener.listenersMux.RUnlock()
		transactionsListener.removeDisconnected()

		log.Printf("Received Blocks: %d, Transactions: %d",
			f.Data.Blocks, f.Data.Transactions)
	}
}

func Transactions(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}
	transactionsListener.register(c)

	for {
		_, _, err := c.ReadMessage()
		if err != nil {
			log.Println("read:", err)
			transactionsListener.unregister(c)
			c.Close()
			break
		}
	}
}

