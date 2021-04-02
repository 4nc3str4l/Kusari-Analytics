"use strict";

import ReconnectingWebsocket from 'reconnecting-websocket';

import React, {Component, Fragment} from "react";

import {EP_GENERAL_STATS} from "../constants";
import TopCard from "./TopCard";

const price = require('crypto-price');

class GeneralStats extends Component {

    constructor(props){
        super(props);
        this.state = {
            currentBlock: 0,
            price: "Fetching...",
        }
        this.ws = null;
    }

    componentWillMount() {
        this.ws = new ReconnectingWebsocket(EP_GENERAL_STATS);
        this.ws.addEventListener('message', this.onDataUpdate.bind(this));
        this.getPrice();
        setInterval(this.getPrice.bind(this), 60000);
    }

    getPrice(){
        let self = this;
        price.getCryptoPrice("USD", "EGLD").then(obj => {
            self.setState({
                ...this.state,
                price: `${parseFloat(obj.price).toFixed(2)}$`
            });
        });
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
        return(
            <Fragment>
                <h4>General Stats</h4>
                <div className={"row"}>

                    <TopCard title={"EGLD Price"}
                         value={this.state.price.toString()}
                         logo={<i className={"fa fa-dollar-sign"}></i>}
                         explanation={"Current Elrond Price"}
                    />

                    <TopCard title={"Average Stake Rewards"}
                         value={this.state.currentBlock.toString()}
                         logo={<i className={"fa fa-layer-group"}></i>}
                         explanation={"Average Stake Rewards"}
                    />

                    <TopCard title={"Current Block Number"}
                         value={this.state.currentBlock.toString()}
                         logo={<i className={"fa fa-th-large"}></i>}
                         explanation={"Current block number"}
                    />

                    <TopCard title={"Average Transaction Cost"}
                         value={this.state.currentBlock.toString()}
                         logo={<i className={"fa fa-gas-pump"}></i>}
                         explanation={"Number of non empty transactions"}
                    />

                    <TopCard title={"Active Users (last 24h)"}
                         value={this.state.currentBlock.toString()}
                         logo={<i className={"fa fa-users"}></i>}
                         explanation={"How many different accounts actively used Elrond in the last 24h"}
                    />

                    <TopCard title={"Smart Contracts"}
                         value={this.state.currentBlock.toString()}
                         logo={<i className={"fa fa-file-signature"}></i>}
                         explanation={"Number of deployed smart contracts"}
                    />

                </div>
            </Fragment>
        );
    }
}

export default GeneralStats;