package main

import (
	"flag"
	"github.com/gorilla/websocket"
	"log"
	"net/http"
)

const address = "0.0.0.0:1212"
var addr = flag.String("addr", address, "http service address")
var upgrader = websocket.Upgrader{} // use default options
var generalStatsListeners = EndpointListeners{}
var transactionsListener = EndpointListeners{}

func main() {
	flag.Parse()
	log.SetFlags(0)

	http.HandleFunc("/", GeneralStats)
	http.HandleFunc("/transactions", Transactions)

	upgrader.CheckOrigin = func(r *http.Request) bool { return true }

	log.Printf("Websocket Server running in %s\n", address)

	// Block number channel
	chBlockNumber := make(chan []byte)

	// Metrics channel
	chTransactions := make(chan []byte)
	go UpdateTransactions(chTransactions)

	// send something to this channel to stop some loops
	closing := make(chan bool)
	go UpdateGeneralStats(chBlockNumber)

	go SetupRabbitMQ(chBlockNumber, chTransactions,  closing)

	log.Fatal(http.ListenAndServe(*addr, nil))
}
