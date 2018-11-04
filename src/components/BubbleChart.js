import React, { Component } from "react";
import "./BubbleChart.css";
import BubbleLines from "./BubbleLines";
import BubbleBoxes from "./BubbleBoxes";

class BubbleChart extends Component {
  

  render() {
    const {data, dataBoxes} = this.props;
    let priorDataBoxes = dataBoxes.filter((boxes, i) => {
    	return boxes.order < 0;
    });
    let currDataBoxes = dataBoxes.filter((boxes, i) => {
    	return boxes.order == 0;
    });
    let postDataBoxes = dataBoxes.filter((boxes, i) => {
    	return boxes.order > 0;
    });

    	// <div style={{position: 'initial'}}>
     //  		<BubbleLines data={data} />
     //  	</div>

    return (
      <div className="window">
      		<div className="half"><BubbleBoxes dataBoxes={priorDataBoxes} /></div>
      		<div className="half" style={{top: '50%'}}><BubbleBoxes dataBoxes={postDataBoxes} /></div>      	
      </div>
    );
  }
}



BubbleChart.defaultProps = {
  data: [],
  dataBoxes: []
};

export default BubbleChart;
