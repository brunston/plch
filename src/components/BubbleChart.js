import React, { Component } from "react";
import "./BubbleChart.css";
import BubbleLines from "./BubbleLines";
import BubbleBoxes from "./BubbleBoxes";

class BubbleChart extends Component {

  my2Callback(dataFromChild) {
  	this.props.callbackFromParent(dataFromChild);
  }

  render() {
    const {data, dataBoxes} = this.props;
    let priorDataBoxes = dataBoxes.filter((boxes, i) => {
    	return boxes.order < 0;
    });
    let postDataBoxes = dataBoxes.filter((boxes, i) => {
    	return boxes.order > 0;
    });

    	// <div style={{position: 'initial'}}>
     //  		<BubbleLines data={data} />
     //  	</div>

    return (
      <div className="window">
      		<div className="half" id="top">
      			<BubbleBoxes dataBoxes={priorDataBoxes} callback2FromParent={this.my2Callback.bind(this)} />
      		</div>
      		<div className="half" id="bottom">
      			<BubbleBoxes dataBoxes={postDataBoxes} callback2FromParent={this.my2Callback.bind(this)} />
      		</div>      	
      </div>
    );
  }
}



BubbleChart.defaultProps = {
  data: [],
  dataBoxes: []
};

export default BubbleChart;
