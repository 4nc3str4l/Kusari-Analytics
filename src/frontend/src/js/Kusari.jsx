"use strict";

import '../scss/style.scss';

import React, {Component, Fragment} from "react";

import TopMenu from "./TopMenu";
import GeneralStats from "./GeneralStats";

class Kusari extends Component {
    
    constructor(props){
        super(props);
    }

    render(){
        return(
            <Fragment>
                <TopMenu />
                <GeneralStats/>
            </Fragment>
        );
    }
}

export default Kusari;