package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type NonceMessage struct {
	Type string `json:"type"`
	Data NonceData `json:"data"`
}

type NonceData struct {
	Nonce uint64 `json:"nonce"`
}

func UpdateGeneralStats(messages chan []byte) {
	generalStatsListeners.initialize()
	var f NonceMessage
	for {
		msg := <- messages
		json.Unmarshal(msg, &f)
		generalStatsListeners.listenersMux.RLock()
		for ws, _ := range generalStatsListeners.listeners {
			_ = ws.WriteJSON(f.Data)
		}
		generalStatsListeners.listenersMux.RUnlock()
		generalStatsListeners.removeDisconnected()

		log.Printf("Received blocknumber: %d", f.Data.Nonce)
	}
}

func GeneralStats(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		return
	}
	generalStatsListeners.register(c)

	for {
		_, _, err := c.ReadMessage()
		if err != nil {
			log.Println("read:", err)
			generalStatsListeners.unregister(c)
			c.Close()
			break
		}
	}
}

