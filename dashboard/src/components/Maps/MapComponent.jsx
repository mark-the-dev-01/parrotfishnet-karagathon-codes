import React, { Component } from "react";
import "./MapComponent.css";
import { GoogleMap, LoadScript } from "@react-google-maps/api";

const center = { lat: 8.545379, lng: 124.566067 };
const APIKEY = "AIzaSyDC2fjGO1xZloKGZnKz6P4NrOkOuS0degc";

export default class MapComponent extends Component {
  render() {
    return (
      <LoadScript googleMapsApiKey={APIKEY}>
        <GoogleMap
          mapContainerClassName="MapComponent"
          center={center}
          zoom={12}
        ></GoogleMap>
      </LoadScript>
    );
  }
}
