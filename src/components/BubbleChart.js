import React, { Component } from "react";
import "./BubbleChart.css";
import BubbleLines from "./BubbleLines";
import BubbleBoxes from "./BubbleBoxes";

class BubbleChart extends Component {
  

  render() {
    const {data} = this.props;
    return (
      <div className="window">
      	<BubbleLines data={data} />
      </div>
    );
  }
}

BubbleChart.defaultProps = {
  data: [],
  dataBoxes: []
};

export default BubbleChart;
