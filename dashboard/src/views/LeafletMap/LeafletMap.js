import React, { Component } from "react";
import "./LeafletMap.css";
import {
  Map,
  TileLayer,
  LayersControl,
  Marker,
  LayerGroup,
  Popup,
  Polyline,
} from "react-leaflet";
import { iconDot } from "components/Icons/Dot/Dot.js";
import logo from "assets/img/noun_Boat_154463.png";
import _ from "lodash";

const { Overlay } = LayersControl;

export default class LeafletMap extends Component {
  state = {
    deviceData: [],
    fishermenData: [],
    lat: 8.545379,
    lng: 124.566067,
    zoom: 15,
  };

  constructor(props) {
    super(props);

    fetch(
      "https://20200825t225841-dot-marine-protected-areas-v279620.et.r.appspot.com/dashboard/api/alldata"
    )
      .then((res) => res.json())
      .then((data) => {
        this.setState({ deviceData: data });
      })
      .catch(console.log);

    fetch(
      "https://20200825t225841-dot-marine-protected-areas-v279620.et.r.appspot.com/dashboard/api/allfishermen"
    )
      .then((res) => res.json())
      .then((data) => {
        this.setState({ fishermenData: data });
      })
      .catch(console.log);
  }

  plotMarkers() {
    let markers = [];

    this.state.deviceData.forEach((device) => {
      let fishermen = this.state.fishermenData.filter(
        (f) => f.identifier == device.device.identifier
      );
      if (fishermen != undefined || fishermen != null) {
        fishermen = fishermen[0];
      }

      const lat = device.telemetry.datapoint.geopoint[0];
      const lng = device.telemetry.datapoint.geopoint[1];
      const popupMessage =
        device.device.name +
        " was " +
        device.telemetry.state +
        " at " +
        device.telemetry.datapoint.FMALocation +
        " " +
        device.telemetry.date_proc_str;
      const date_proc = device.telemetry.date_proc;
      markers.push({
        key: date_proc.toString(),
        device_key: device.device.identifier,
        content: popupMessage,
        position: [lat, lng],
        icon: iconDot,
      });
    });

    return markers;
  }

  groupMarkers() {
    let list = [];
    let i = 0;
    const groups = _.groupBy(this.state.deviceData, "device.identifier");
    for (const k in groups) {
      if (groups.hasOwnProperty(k)) {
        let positions = groups[k].map((m) => m.telemetry.datapoint.geopoint);

        list.push({
          index: i,
          key: groups[k][0].device.name,
          markerArray: groups[k],
          markerList: this.popupMarker(groups[k]),
          positions: positions,
          polylineOptions: {
            color: "red",
            weight: 6,
            opacity: 0.9,
          },
        });
        i++;
      }
    }

    return list.map((marker) => (
      <Overlay key={"overlay-" + marker.index} name={marker.key} checked>
        <LayerGroup key={"layer-group-" + marker.index}>
          {marker.markerList}
          <Polyline
            positions={marker.positions}
            options={marker.polylineOptions}
          ></Polyline>
        </LayerGroup>
      </Overlay>
    ));
  }

  popupMarker(markers) {
    markers.forEach((element) => {
      let fishermen = this.state.fishermenData.filter(
        (f) => f.identifier == element.device.identifier
      );
      if (fishermen != undefined || fishermen != null) {
        fishermen = fishermen[0];
      }

      element.fisherman_data = fishermen;
      element.content =
        element.device.name +
        " was " +
        element.telemetry.state +
        " at " +
        element.telemetry.datapoint.FMALocation +
        " " +
        element.telemetry.date_proc_str;
      element.position = element.telemetry.datapoint.geopoint;
      element.icon = iconDot;
    });

    console.log(markers);

    return markers.map((marker) => (
      <Marker key={marker.id} position={marker.position} icon={marker.icon}>
        <Popup>
          <img
            src={logo}
            alt="Boat by Fabián Sanabria from the Noun Project"
            width="50%"
            className="classes.img"
          />
          <div>
            <p>
              <b>Name: </b>
              {(marker.fisherman_data || { owner: "" }).owner}
            </p>
            <p>
              <b>Address: </b>
              {(marker.fisherman_data || { address: "" }).address}
            </p>
            <p>
              <b>Contact Number: </b>
              {(marker.fisherman_data || { contact_number: "" }).contact_number}
            </p>
            <p>
              <b>Family Number: </b>
              {(marker.fisherman_data || { familiy_number: "" }).familiy_number}
            </p>
            <p>
              <b>Location: </b>
              {marker.telemetry.datapoint.geopoint.join()}
            </p>
          </div>
        </Popup>
      </Marker>
    ));
  }

  render() {
    let plottedMarkers = [];
    let groupedMarkers = null;
    if (this.state.deviceData.length > 0) {
      plottedMarkers = this.plotMarkers();
      groupedMarkers = this.groupMarkers();
    }
    const position = [this.state.lat, this.state.lng];

    return (
      <Map
        center={position}
        zoom={this.state.zoom}
        className="Leaflet-map-container"
      >
        <LayersControl position="topright">
          <TileLayer
            attribution='&amp;copy <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {groupedMarkers}
        </LayersControl>
      </Map>
    );
  }
}
