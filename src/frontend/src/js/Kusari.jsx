"use strict";

import '../scss/style.scss';

import React, {Component, Fragment} from "react";
import GeneralStats from "./GeneralStats";

class Kusari extends Component {
    
    constructor(props){
        super(props);
    }

    render(){
        return(
            <Fragment>
                <h1>Hello Elrond</h1>
                <GeneralStats/>
            </Fragment>

        );
    }
}

export default Kusari;