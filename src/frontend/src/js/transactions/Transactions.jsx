"use strict";

import ReconnectingWebsocket from 'reconnecting-websocket';

import React, {Component, Fragment} from "react";

import {EP_TRANSACTIONS} from "../constants";
import TopCard from "../components/TopCard";


class Transactions extends Component {

    constructor(props){
        super(props);
        this.state = {
            transaction24h: 0,
            blocks24h: 0
        }
        this.ws = null;
    }

    componentWillMount() {
        this.ws = new ReconnectingWebsocket(EP_TRANSACTIONS);
        this.ws.addEventListener('message', this.onDataUpdate.bind(this));
    }


    onDataUpdate(message){
        let packet = JSON.parse(message.data);
        this.setState({
            ...this.state,
            blocks24h: packet.rolling_24_blocks,
            transaction24h: packet.rolling_24_txs
        })
    }

    componentWillUnmount() {
        this.ws.removeEventListener('message', this.onDataUpdate.bind(this));
        this.ws.close();
    }

    render(){
        return(
            <Fragment>
                <h4>Transactions</h4>
                <div className={"row"}>

                    <TopCard title={"Num Blocks (last 24h)"}
                             value={this.state.blocks24h.toString()}
                             logo={<i className={"fa fa-users"}></i>}
                             explanation={"How many different accounts actively used Elrond in the last 24h"}
                    />

                    <TopCard title={"Num Transactions (24)"}
                             value={this.state.transaction24h.toString()}
                             logo={<i className={"fa fa-file-signature"}></i>}
                             explanation={"Number of deployed smart contracts"}
                    />

                </div>
            </Fragment>
        );
    }
}

export default Transactions;