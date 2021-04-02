"use strict";

import React, {Component} from "react";
import PropTypes from "prop-types";

class TopCard extends Component{

    constructor(props) {
        super(props);
    }

    render(){
        return(
            <div className={"col col-md-4"}>
                <div className={"kusari-card"} title={this.props.explanation}>
                    <p className={"kusari-card-title"}>{this.props.title}</p>
                    <span className={"kusari-card-value"}>{this.props.value}</span>
                    <div className={"kusari-card-logo"}>{this.props.logo} </div>
                </div>
            </div>
        )
    }
}

export default TopCard;

TopCard.propTypes = {
    title: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    logo: PropTypes.object.isRequired,
    explanation: PropTypes.string.isRequired,

}