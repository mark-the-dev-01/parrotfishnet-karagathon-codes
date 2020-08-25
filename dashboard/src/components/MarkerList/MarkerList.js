import React, { Component } from "react";
import { Marker, Popup } from "react-leaflet";
import logo from "assets/img/noun_Boat_154463.png";
import _ from "lodash";
import { iconDot } from "components/Icons/Dot/Dot.js";

const PopupMarker = ({ content, position, icon }) => (
  <Marker position={position} icon={icon}>
    <Popup>
      <img
        src={logo}
        alt="Boat by Fabián Sanabria from the Noun Project"
        className="classes.img"
      />
      <div>{content}</div>
    </Popup>
  </Marker>
);

export default class MarkerList extends Component {
  state = {};

  render() {
    console.log(this.props.markers);
    this.props.markers.forEach((element) => {
      element.content = "content";
      element.position = element.telemetry.datapoint.geopoint;
      element.icon = iconDot;
    });

    return this.props.markers.map((id, content, position, icon) => (
      <PopupMarker
        key={id.id}
        content={content}
        position={position}
        icon={icon}
      ></PopupMarker>
    ));
  }
}
// inspired by https://github.com/PaulLeCam/react-leaflet/blob/master/example/components/custom-component.js
// https://stackoverflow.com/questions/43948828/how-to-pass-an-array-of-items-in-react-js
