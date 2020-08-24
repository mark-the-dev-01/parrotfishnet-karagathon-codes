import React, { Component } from "react";
import { Marker, Popup } from "react-leaflet";
import logo from "assets/img/noun_Boat_154463.png";

const PopupMarker = ({ content, position, icon }) => (
  <Marker position={position} icon={icon}>
    <Popup>
      <img
        src={logo}
        alt="Boat by Fabián Sanabria from the Noun Project"
        width="25%"
        className="classes.img"
      />
      <div>{content}</div>
    </Popup>
  </Marker>
);

export default class MarkerList extends Component {
  state = {};

  render() {
    return this.props.markers.map(({ key, ...props }) => (
      <PopupMarker key={key} {...props}></PopupMarker>
    ));
  }
}
// inspired by https://github.com/PaulLeCam/react-leaflet/blob/master/example/components/custom-component.js
// https://stackoverflow.com/questions/43948828/how-to-pass-an-array-of-items-in-react-js
