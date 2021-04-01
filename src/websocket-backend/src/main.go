package main

import (
	"encoding/json"
	"flag"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
)

const address = "0.0.0.0:1212"

var addr = flag.String("addr", address, "http service address")

var upgrader = websocket.Upgrader{} // use default options

var generalStatsListeners = EndpointListeners{}

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

func main() {
	flag.Parse()
	log.SetFlags(0)
	http.HandleFunc("/", GeneralStats)
	upgrader.CheckOrigin = func(r *http.Request) bool { return true }

	log.Printf("Websocket Server running in %s\n", address)

	messages := make(chan []byte)

	// send something to this channel to stop some loops
	closing := make(chan bool)

	go SetupRabbitMQ(messages, closing)
	go UpdateGeneralStats(messages)
	log.Fatal(http.ListenAndServe(*addr, nil))
}
