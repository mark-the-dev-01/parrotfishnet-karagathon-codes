import React from "react";
import "./LeafletMap.css";
import { Map, TileLayer, Marker, Popup } from "react-leaflet";

export default function LeafletMap() {
  const mapState = {
    lat: 8.545379,
    lng: 124.566067,
    zoom: 11,
  };
  const position = [mapState.lat, mapState.lng];

  return (
    <Map
      center={position}
      zoom={mapState.zoom}
      className="Leaflet-map-container"
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
