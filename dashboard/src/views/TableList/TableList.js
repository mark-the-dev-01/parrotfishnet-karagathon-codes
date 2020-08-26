import React, { Component } from "react";
// @material-ui/core components
import { makeStyles } from "@material-ui/core/styles";
// core components
import GridItem from "components/Grid/GridItem.js";
import GridContainer from "components/Grid/GridContainer.js";
import Table from "components/Table/Table.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardBody from "components/Card/CardBody.js";

const styles = {
  cardCategoryWhite: {
    "&,& a,& a:hover,& a:focus": {
      color: "rgba(255,255,255,.62)",
      margin: "0",
      fontSize: "14px",
      marginTop: "0",
      marginBottom: "0",
    },
    "& a,& a:hover,& a:focus": {
      color: "#FFFFFF",
    },
  },
  cardTitleWhite: {
    color: "#FFFFFF",
    marginTop: "0px",
    minHeight: "auto",
    fontWeight: "300",
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    marginBottom: "3px",
    textDecoration: "none",
    "& small": {
      color: "#777",
      fontSize: "65%",
      fontWeight: "400",
      lineHeight: "1",
    },
  },
};

export default class TableList extends Component {
  state = {
    classes: makeStyles(styles),
    deviceData: [],
    groupedData: [],
    tableData: {
      Triggers: {
        title: "Fisherman Location Tracked",
        subTitle: "List of times we have the vessel location.",
        tableHeader: ["Time Tracked", "Vessel name", "FMA", "FMZ"],
      },
    },
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
  }

  groupDeviceData() {
    ["Triggers"].forEach((element) => {
      let d = [];
      switch (element) {
        default:
          this.state.deviceData
            .sort((a, b) => b.telemetry.date_proc - a.telemetry.date_proc)
            .forEach((dev) => {
              if (dev.telemetry.state === "triggered") {
                d.push([
                  dev.telemetry.date_proc_str,
                  dev.device.name,
                  dev.telemetry.datapoint.FMALocation,
                  dev.telemetry.datapoint.FMZ,
                ]);
              }
            });
          break;
      }

      this.state.groupedData.push({
        title: this.state.tableData[element].title,
        subTitle: this.state.tableData[element].subTitle,
        header: this.state.tableData[element].tableHeader,
        data: d,
      });
    });
  }

  render() {
    if (this.state.deviceData.length > 0) {
      this.groupDeviceData();
    }

    return (
      <GridContainer>
        <GridItem xs={12} sm={12} md={12}>
          <Card>
            <CardHeader color="primary">
              <h4 className={this.state.classes.cardTitleWhite}>
                {(this.state.groupedData[0] || { title: "" }).title}
              </h4>
              <p className={this.state.classes.cardCategoryWhite}>
                {(this.state.groupedData[0] || { subTitle: "" }).subTitle}
              </p>
            </CardHeader>
            <CardBody>
              <Table
                tableHeaderColor="primary"
                tableHead={(this.state.groupedData[0] || { header: [] }).header}
                tableData={(this.state.groupedData[0] || { data: [] }).data}
              />
            </CardBody>
          </Card>
        </GridItem>
      </GridContainer>
    );
  }
}
