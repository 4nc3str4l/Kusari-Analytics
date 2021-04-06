"use strict";

import React, {Component} from "react";
import PropTypes from "prop-types";


class DataTable extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <table className={"table"}>
                <thead>
                    <tr>
                        {this.rendertitles()}
                    </tr>
                </thead>
                <tbody>
                    {this.renderContent()}
                </tbody>
            </table>
        )
    }

    rendertitles(){
        if(typeof this.props.titles === 'undefined'){
            return (null);
        }
        let h = [];
        for(let i = 0; i < this.props.titles.length; ++i){
            h.push(<th key={i}>{this.props.titles[i]}</th>)
        }
        return h;
    }

    renderContent(){
        if(typeof this.props.titles === 'undefined' || 
            typeof this.props.contents === 'undefined' || 
            this.props.contents.length === 0){
            return(
                <tr>
                    <td>No data</td>
                </tr>
            )
        }

        let rows = [];
        for(let i = 0; i < this.props.contents.length; ++i){
            rows.push(<tr key={i}>{this.renderRowContent(this.props.contents[i])}</tr>)
        }

        return rows;
    }

    renderRowContent(rowData){
        let columns = [];
        for(let col = 0; col < rowData.length; ++col){
            columns.push(<td key={col}>{rowData[col]}</td>);
        }
        return columns;
    }
}

DataTable.propTypes = {
    titles: PropTypes.array.isRequired,
    contents: PropTypes.array.isRequired
}

export default DataTable;