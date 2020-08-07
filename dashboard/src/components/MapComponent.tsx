import { GoogleMap, LoadScript } from "@react-google-maps/api";
import React from "react";

const containerStyle = {
  width: "400px",
  height: "400px",
};

const center = {
  lat: -3.745,
  lng: -38.523,
};

function MapComponent() {
  return <div className="map">null</div>;
}

export default React.memo(MapComponent);
