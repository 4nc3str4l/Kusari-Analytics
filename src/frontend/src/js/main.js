import Kusari from './Kusari';

import React from 'react';
import ReactDOM from 'react-dom'

const wrapper = document.getElementById("kusari");

wrapper ? ReactDOM.render(<Kusari/>, wrapper) : false;