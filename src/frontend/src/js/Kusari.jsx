"use strict";

import '../scss/style.scss';

import React, {Component, Fragment} from "react";

import TopMenu from "./TopMenu";
import GeneralStats from "./general-stats/GeneralStats";
import Economics from "./economics/Economics";
import Transactions from "./transactions/Transactions";

class Kusari extends Component {
    
    constructor(props){
        super(props);
    }

    render(){
        return(
            <Fragment>
                <TopMenu />
                <div className={"content"}>
                    <GeneralStats/>
                    <Economics />
                    <Transactions />
                </div>
            </Fragment>
        );
    }
}

export default Kusari;