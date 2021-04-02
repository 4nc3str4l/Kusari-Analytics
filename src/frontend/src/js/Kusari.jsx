"use strict";

import '../scss/style.scss';

import React, {Component, Fragment} from "react";

import TopMenu from "./TopMenu";
import GeneralStats from "./general-stats/GeneralStats";

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
                </div>
            </Fragment>
        );
    }
}

export default Kusari;