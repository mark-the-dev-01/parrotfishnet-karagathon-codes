import React, { Component, Fragment } from "react";
import { Marker, Popup } from "react-leaflet";

const PopupMarker = ({ content, position }) => (
  <Marker position={position}>
    <Popup>{content}</Popup>
  </Marker>
);

export default class MarkerList extends Component {
  state = {};

  render() {
    // const items = this.props.markers.map(({ key, ...props }) => (
    return this.props.markers.map(({ key, ...props }) => (
      <PopupMarker key={key} {...props}></PopupMarker>
    ));

    // return <Fragment>{items}</Fragment>;
  }
}
// inspired by https://github.com/PaulLeCam/react-leaflet/blob/master/example/components/custom-component.js
// https://stackoverflow.com/questions/43948828/how-to-pass-an-array-of-items-in-react-js
