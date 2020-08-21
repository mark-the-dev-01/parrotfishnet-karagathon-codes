import React, { Component } from "react";
import "./LeafletMap.css";
import { Map, TileLayer } from "react-leaflet";
import MarkerList from "../../components/MarkerList/MarkerList.js";
import { LayerGroup } from "leaflet";

export default class LeafletMap extends Component {
  state = {
    deviceData: [],
    lat: 8.545379,
    lng: 124.566067,
    zoom: 13,
  };

  constructor(props) {
    super(props);

    fetch(
      "https://20200820t223325-dot-marine-protected-areas-v279620.et.r.appspot.com/dashboard/api/alldata"
    )
      .then((res) => res.json())
      .then((data) => {
        this.setState({ deviceData: data });
      })
      .catch(console.log);
    console.log("tableList constructor");
  }

  plotMarkers() {
    let markers = [];

    this.state.deviceData.forEach((device) => {
      const lat = device.telemetry.datapoint.geopoint[0];
      const lng = device.telemetry.datapoint.geopoint[1];
      const popupMessage =
        device.device.name +
        " was " +
        device.telemetry.state +
        " " +
        device.telemetry.date_proc_str;
      const date_proc = device.telemetry.date_proc;
      markers.push({
        key: date_proc.toString(),
        content: popupMessage,
        position: [lat, lng],
      });
    });

    return markers;
  }

  render() {
    let markers = [];
    if (this.state.deviceData.length > 0) {
      markers = this.plotMarkers();
    }
    const position = [this.state.lat, this.state.lng];

    return (
      <Map
        center={position}
        zoom={this.state.zoom}
        className="Leaflet-map-container"
      >
        <TileLayer
          attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <MarkerList markers={markers}></MarkerList>
      </Map>
    );
  }
}
