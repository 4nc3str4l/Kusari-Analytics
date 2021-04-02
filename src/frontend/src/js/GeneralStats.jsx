"use strict";

import ReconnectingWebsocket from 'reconnecting-websocket';

import React, {Component, Fragment} from "react";

import {EP_GENERAL_STATS} from "./constants";

class GeneralStats extends Component {

    constructor(props){
        super(props);

        this.state = {
            currentBlock: 0
        }
        this.ws = null;
    }

    componentWillMount() {
        this.ws = new ReconnectingWebsocket(EP_GENERAL_STATS);
        this.ws.addEventListener('message', this.onDataUpdate.bind(this));
    }

    onDataUpdate(message){
        let packet = JSON.parse(message.data);
        this.setState({
            ...this.state,
            currentBlock: packet.nonce
        })
    }

    componentWillUnmount() {
        this.ws.removeEventListener('message', this.onDataUpdate.bind(this));
        this.ws.close();
    }

    render(){
        return(<p>Current block {this.state.currentBlock}</p>);
    }
}

export default GeneralStats;