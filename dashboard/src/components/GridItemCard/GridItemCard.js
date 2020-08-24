import React, { Component } from "react";

import Update from "@material-ui/icons/Update";

import GridItem from "components/Grid/GridItem.js";
import Card from "components/Card/Card.js";
import CardHeader from "components/Card/CardHeader.js";
import CardIcon from "components/Card/CardIcon.js";
import CardFooter from "components/Card/CardFooter.js";

export default class GridItemCard extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <GridItem
        xs={this.props.cardValue.gridItemSizes.xs}
        sm={this.props.cardValue.gridItemSizes.sm}
        md={this.props.cardValue.gridItemSizes.md}
      >
        <Card>
          <CardHeader color={this.props.cardValue.cardInfoColor} stats icon>
            <CardIcon color={this.props.cardValue.cardInfoColor}>
              {this.props.cardValue.cardIconContent}
            </CardIcon>
            <p className={this.props.classes.cardCategory}>
              {this.props.cardValue.title}
            </p>
            <h3 className={this.props.classes.cardTitle}>
              {this.props.cardValue.value}
            </h3>
          </CardHeader>
          <CardFooter stats>
            <div className={this.props.classes.stats}>
              <Update />
              {this.props.cardValue.footerTitle}
            </div>
          </CardFooter>
        </Card>
      </GridItem>
    );
  }
}
