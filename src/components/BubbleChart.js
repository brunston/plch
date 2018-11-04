import React, { Component } from "react";
import "./BubbleChart.css";
import BubbleBoxes from "./BubbleBoxes";

class BubbleChart extends Component {
  constructor(props) {
    super(props);
    this.state = {
      priorDataBoxes: [],
      postDataBoxes: []
    };
  }

  my2Callback(dataFromChild) {
    this.props.callbackFromParent(dataFromChild);
  	const { data, dataBoxes } = this.props;
    this.state.priorDataBoxes = dataBoxes.filter((boxes, i) => {
      return boxes.order < dataFromChild.order;
    });
    this.state.postDataBoxes = dataBoxes.filter((boxes, i) => {
      return boxes.order > dataFromChild.order;
    });
    console.log(this.state.priorDataBoxes);
  }

  render() {
  	const { data, dataBoxes } = this.props;
    this.state.priorDataBoxes = dataBoxes.filter((boxes, i) => {
      return boxes.order < 20;
    });
    this.state.postDataBoxes = dataBoxes.filter((boxes, i) => {
      return boxes.order > 20;
    });
    

    // <div style={{position: 'initial'}}>
    //  		<BubbleLines data={data} />
    //  	</div>

    return (
      <div className="window">
        <div className="half" id="top">
          <BubbleBoxes
            dataBoxes={this.state.priorDataBoxes}
            callback2FromParent={this.my2Callback.bind(this)}
          />
        </div>
        <div className="half" id="bottom">
          <BubbleBoxes
            dataBoxes={this.state.postDataBoxes}
            callback2FromParent={this.my2Callback.bind(this)}
          />
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
