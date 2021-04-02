package main

import (
	"fmt"
	"github.com/gorilla/websocket"
	"log"
	"sync"
)

type EndpointListeners struct {
	listeners    map[*websocket.Conn]bool
	listenersMux sync.RWMutex

	needsCleaning bool
	cleaningMux sync.RWMutex
}

func (ep* EndpointListeners) initialize() {
	ep.listeners = make(map[*websocket.Conn]bool)
	ep.needsCleaning = false
}

func (ep* EndpointListeners) register(c *websocket.Conn){
	ep.listenersMux.Lock()
	ep.listeners[c] = true
	log.Printf("Number of clients %d\n", len(ep.listeners))
	ep.listenersMux.Unlock()
}

func (ep* EndpointListeners)  unregister (c *websocket.Conn){
	ep.listenersMux.Lock()
	ep.listeners[c] = false
	ep.listenersMux.Unlock()

	ep.setNeedsCleaning(true)
}

func (ep* EndpointListeners) removeDisconnected (){
	if !ep.readNeedsCleaning(){
		return
	}

	ep.listenersMux.Lock()
	for ws, connected := range ep.listeners {
		if connected == false {
			delete(ep.listeners, ws)
			fmt.Println("Disconnected!")
		}
	}
	log.Printf("Number of clients %d\n", len(ep.listeners))
	ep.listenersMux.Unlock()

	ep.setNeedsCleaning(false)
}

func (ep* EndpointListeners) setNeedsCleaning (isCleaningNeeded bool){
	ep.cleaningMux.Lock()
	ep.needsCleaning = isCleaningNeeded
	ep.cleaningMux.Unlock()
}

func (ep* EndpointListeners) readNeedsCleaning () bool {
	ep.cleaningMux.RLock()
	toReturn := ep.needsCleaning
	ep.cleaningMux.RUnlock()
	return toReturn
}