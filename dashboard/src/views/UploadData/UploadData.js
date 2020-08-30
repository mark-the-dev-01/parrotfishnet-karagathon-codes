import React, { Component } from "react";

import { withStyles } from "@material-ui/core/styles";
import PropTypes from "prop-types";
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Tasks from "components/Tasks/Tasks.js";
import CustomTabs from "components/CustomTabs/CustomTabs.js";
import Info from "components/Typography/Info.js";
import Danger from "components/Typography/Danger.js";
import Success from "components/Typography/Success.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardBody from "components/Card/CardBody.js";
import CardFooter from "components/Card/CardFooter.js";

import Update from "@material-ui/icons/Update";
import Lens from "@material-ui/icons/Lens";
import Warning from "@material-ui/icons/Warning";
import Icon from "@material-ui/core/Icon";
import Check from "@material-ui/icons/Check";

import styles from "assets/jss/material-dashboard-react/views/dashboardStyle.js";
import "./UploadData.css";

import _ from "lodash";
import axios from "axios";

class UploadData extends Component {
  state = {
    mapDataUpload: false,
    mapUploadResult: <Lens />,
    selectedFileForMap: null,
    fishermanDataUpload: false,
    selectedFileForFishermen: null,
  };
  onMapFileChange = (event) => {
    this.setState({
      selectedFileForMap: event.target.files[0],
      mapUploadResult: (
        <Info>
          <Update />
          <span>Preparing data for map upload</span>
        </Info>
      ),
    });
  };

  onMapFileUpload = () => {
    var self = this;
    const formData = new FormData();

    // Update the formData object
    formData.append(
      "mapdata",
      this.state.selectedFileForMap,
      this.state.selectedFileForMap.name
    );

    // Details of the uploaded file
    console.log(this.state.selectedFileForMap);

    axios
      .post(
        "https://20200827t003648-dot-marine-protected-areas-v279620.et.r.appspot.com/dashboard/api/addmapdata",
        formData
      )
      .then(function (response) {
        // handle success
        if (response.data.result) {
          alert("upload complete");
          document.getElementById("mapdata").value = "";
          self.setState({
            mapUploadResult: (
              <Success>
                <Check />
                <span>Upload for map file is completed</span>
              </Success>
            ),
          });
        } else {
          self.setState({
            mapUploadResult: (
              <Danger>
                <Warning />
                <span>Upload for map file is incompleted.</span>
              </Danger>
            ),
          });
        }
      });
  };

  render() {
    const { classes } = this.props;

    return (
      <GridContainer>
        <GridItem xs={12} sm={6} md={6}>
          <Card>
            <CardHeader color="info" stats icon>
              <CardIcon color="info">
                <Icon>location_on</Icon>
              </CardIcon>
              <p className={classes.cardCategory}>Upload Map Data</p>
              <h3 className={classes.cardTitle + " uploadData"}>
                <small>
                  <input
                    type="file"
                    name="mapdata"
                    id="mapdata"
                    onChange={this.onMapFileChange}
                  />
                  <button onClick={this.onMapFileUpload}>Upload</button>
                </small>
              </h3>
            </CardHeader>
            <CardFooter stats>
              <div className={classes.stats}>{this.state.mapUploadResult}</div>
            </CardFooter>
          </Card>
        </GridItem>
      </GridContainer>
    );
  }
}

UploadData.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(UploadData);
