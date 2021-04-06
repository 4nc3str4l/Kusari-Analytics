"use strict";

import React, {Component, Fragment} from "react";
import {XAxis, YAxis, ResponsiveContainer, Tooltip, Area, AreaChart} from 'recharts';
import DataTable from "../components/DataTable";

const data = [
    {
        "name": "< 1",
        "pv": 100,
    },
    {
        "name": "1-10",
        "pv": 80,
    },
    {
        "name": "10-50",
        "pv": 60,
    },
    {
        "name": "50-100",
        "pv": 40,
    },
    {
        "name": "100-500",
        "pv": 20,
    },
    {
        "name": "500-1K",
        "pv": 15,
    },
    {
        "name": "1K-5K",
        "pv": 10,
    },
    {
        "name": "5K-10K",
        "pv": 6,
    },
    {
        "name": "10k-50k",
        "pv": 7,
    },
    {
        "name": "50k-100K",
        "pv": 7,
    },
    {
        "name": "100k-1M",
        "pv": 7,
    },
    {
        "name": "> 1M",
        "pv": 2,
    },
]


const walletActivity = [
    {
        "name": "< 1",
        "pv": 3000,
    },
    {
        "name": "1-10",
        "pv": 80,
    },
    {
        "name": "10-50",
        "pv": 60,
    },
    {
        "name": "50-100",
        "pv": 456,
    },
    {
        "name": "100-500",
        "pv": 20,
    },
    {
        "name": "500-1K",
        "pv": 500,
    },
    {
        "name": "1K-5K",
        "pv": 10,
    },
    {
        "name": "5K-10K",
        "pv": 6,
    },
    {
        "name": "10k-50k",
        "pv": 7,
    },
    {
        "name": "50k-100K",
        "pv": 200,
    },
    {
        "name": "100k-1M",
        "pv": 250,
    },
    {
        "name": "> 1M",
        "pv": 4000,
    },
]

class Economics extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Fragment>
                <div className={"row m30px"}>
                    <div className={"col col-md-6"}>
                        <h4>Wealth Distribution</h4>
                        <ResponsiveContainer height={250} width='100%'>
                            <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#ffffff" stopOpacity={0.8}/>
                                        <stop offset="95%" stopColor="#0e131d" stopOpacity={0}/>
                                    </linearGradient>
                                </defs>
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Area type="monotone" dataKey="pv" stroke="#ffffff" fillOpacity={1} fill="url(#colorPv)" />
                            </AreaChart>
                        </ResponsiveContainer>
                        <p className={"plot-explanation"}> Num wallets vs wealth </p>
                    </div>

                    <div className={"col col-md-6"}>
                        <h4>Wallet Activity</h4>
                        <ResponsiveContainer height={250} width='100%'>
                            <AreaChart data={walletActivity} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                                <defs>
                                    <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#ffffff" stopOpacity={0.8}/>
                                        <stop offset="95%" stopColor="#0e131d" stopOpacity={0}/>
                                    </linearGradient>
                                </defs>
                                <XAxis dataKey="name" />
                                <YAxis />
                                <Area type="monotone" dataKey="pv" stroke="#ffffff" fillOpacity={1} fill="url(#colorPv)" />
                            </AreaChart>
                        </ResponsiveContainer>
                        <p className={"plot-explanation"}>Tx per day vs Wealth</p>
                    </div>
                </div>
                <div className={"row m30px"}>

                    <div className={"col col-md-6"}>
                        <h4>Latest Wale Transactions (24h)</h4>
                        <br />
                        <DataTable
                            titles={["Timestamp", "Amount (EGLD)", "Tx Id"]}
                            contents={[
                                ["15:59:23", "10'000", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>],
                                ["16:12:23", "3'030", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>],
                                ["16:12:23", "3'030", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>],
                                ["16:12:23", "3'030", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>],
                                ["16:12:23", "3'030", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>],
                                ["16:12:23", "3'030", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>],
                                ["16:12:23", "3'030", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>],
                                ["16:12:23", "3'030", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>],
                                ["19:12:23", "2'050", <a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>]]}
                        />
                    </div>

                    <div className={"col col-md-6"}>
                        <h4>Most Active Addresses (24h)</h4>
                        <br />
                        <DataTable
                            titles={["Address", "Num Transactions", "EGLD Balance"]}
                            contents={[
                                [<a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>, "15'232", "123'123"],
                                [<a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>, "15'232", "123'123"],
                                [<a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>, "15'232", "123'123"],
                                [<a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>, "15'232", "123'123"],
                                [<a href={"https://explorer.elrond.com/transactions/047e71625b0789fcfdcb008e48f2e10c77359fb176d33c6e6c5980146321cb6b"}>047e71625b...cb6</a>, "15'232", "123'123"]]}
                        />
                    </div>
                </div>
                
            </Fragment>
        )
    }

}

export default Economics;