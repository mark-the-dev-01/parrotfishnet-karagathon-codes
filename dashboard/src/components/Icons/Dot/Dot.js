import L from "leaflet";

const iconDot = new L.Icon({
  iconUrl: require("../../../assets/img/dot_PNG36_25px.png"),
  iconRetinaUrl: require("../../../assets/img/dot_PNG36_25px.png"),
  //   iconAnchor: null,
  //   popupAnchor: null,
  //   shadowUrl: null,
  //   shadowSize: null,
  //   shadowAnchor: null,
  iconSize: new L.Point(25, 25),
  //   className: "leaflet-div-icon",
});

export { iconDot };
