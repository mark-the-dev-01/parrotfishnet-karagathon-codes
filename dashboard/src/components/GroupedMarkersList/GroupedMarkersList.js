import React, { Component } from "react";
import { Marker, Popup, LayerGroup, LayersControl } from "react-leaflet";
import _ from "lodash";
import MarkerList from "components/MarkerList/MarkerList.js";

const { Overlay } = LayersControl;

export default class GroupedMarkersList extends Component {
  groupMarkers() {
    const groups = _.groupBy(this.props.markers, "device_key");
    let markerList = [];
    for (const k in groups) {
      if (groups.hasOwnProperty(k)) {
        markerList.push({ key: k, markers: groups[k] });
      }
    }

    return markerList;
  }

  render() {
    // return _.groupBy(this.props.markers, ["device_key"]).map(
    //   (markers, device_key) => (
    //     <Overlay key={device_key} name={device_key}>
    //       <LayerGroup>
    //         <MarkerList markers={markers}></MarkerList>
    //       </LayerGroup>
    //     </Overlay>
    //   )
    // );

    // for (x in _.groupBy(temp1, "device_key")) { console.log(_.groupBy(temp1, "device_key")[x]) }
    let markerList = this.groupMarkers();

    // const markerList = _.chain(this.props.markers)
    //   .groupBy(function (i) {
    //     return i.device_key;
    //   })
    //   .map(function (values, key) {
    //     return { key: key.replace("-", ""), markers: values };
    //   })
    //   .value();

    console.log(this.props.markers);
    console.log(_.VERSION);
    console.log(markerList);

    // return <div>somethign</div>;

    return markerList.map(({ key, markers }) => (
      //   <Overlay key={key} name={key}>
      //     <LayerGroup>
      <MarkerList key={key} markers={markers}></MarkerList>
      //     </LayerGroup>
      //   </Overlay>
    ));
  }
}
