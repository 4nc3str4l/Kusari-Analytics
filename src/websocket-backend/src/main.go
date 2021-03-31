package main

import (
	"flag"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
	"time"
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

type GeneralInfo struct {
	BlockNumber      int    `json:"block_num"`
}

func UpdateGeneralStats() {
	generalStatsListeners.initialize()
	gi := GeneralInfo{0}
	for {
		generalStatsListeners.listenersMux.RLock()
		for ws, _ := range generalStatsListeners.listeners {
			_ = ws.WriteJSON(gi)
		}
		generalStatsListeners.listenersMux.RUnlock()
		generalStatsListeners.removeDisconnected()
		gi.BlockNumber++
		time.Sleep(1 * time.Second)
	}
}

func main() {
	flag.Parse()
	log.SetFlags(0)
	http.HandleFunc("/", GeneralStats)
	upgrader.CheckOrigin = func(r *http.Request) bool { return true }

	log.Printf("Websocket Server running in %s\n", address)
	go UpdateGeneralStats()
	log.Fatal(http.ListenAndServe(*addr, nil))
}
