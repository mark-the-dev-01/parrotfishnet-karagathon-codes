import React, { Component } from "react";
import { Map, TileLayer, Marker, Popup } from "react-leaflet";

export default class LeafletMap extends Component {
  state = {
    lat: 8.545379,
    lng: 124.566067,
    zoom: 11,
  };

  render() {
    const position = [this.state.lat, this.state.lng];

    return (
      <Map
        center={position}
        zoom={this.state.zoom}
        style={{ width: "100%", height: "500px" }}
      >
        <TileLayer
          attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Marker position={position}>
          <Popup>a pretty customizable CSS3 popup.</Popup>
        </Marker>
      </Map>
    );
  }
}
