package main

import (
	"flag"
	"log"
	"net/http"

	"github.com/gorilla/websocket"
)

const address = "0.0.0.0:1212"

var addr = flag.String("addr", address, "http service address")

var upgrader = websocket.Upgrader{} // use default options

func GeneralStats(w http.ResponseWriter, r *http.Request) {
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Print("upgrade:", err)
		return
	}
	defer c.Close()
	for {
		mt, message, err := c.ReadMessage()
		if err != nil {
			log.Println("read:", err)
			break
		}
		log.Printf("recv: %s", message)
		err = c.WriteMessage(mt, message)
		if err != nil {
			log.Println("write:", err)
			break
		}
	}
}

func main() {
	flag.Parse()
	log.SetFlags(0)
	http.HandleFunc("/", GeneralStats)
	upgrader.CheckOrigin = func(r *http.Request) bool { return true }

	log.Printf("Websocket Server running in %s\n", address)
	log.Fatal(http.ListenAndServe(*addr, nil))
}
