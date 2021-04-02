"use strict";

import React, {Component} from "react";

// const MENU_SECTIONS = [["General Stats", "#"]];
const MENU_SECTIONS = [];

class TopMenu extends Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <nav className="navbar navbar-expand-lg">
                <a className="navbar-brand" href="#"><span class="kusari-logo">鎖</span> Kusari Analytics</a>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText"
                        aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarText">
                    <ul className="navbar-nav mr-auto">
                        {this.renderSectionList()}
                    </ul>
                </div>

            </nav>
        );
    }

    renderSectionList(){
        const sections = [];
        let s;
        for(let i = 0; i < MENU_SECTIONS.length; ++i){
            s = MENU_SECTIONS[i];
            sections.push(
                <li className="nav-item active">
                    <a className="nav-link" href={s[1]}>{s[0]}<span className="sr-only">(current)</span></a>
                </li>
            )
        }
        return sections;
    }
}

export default TopMenu;