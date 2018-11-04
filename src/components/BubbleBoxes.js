import React, { Component } from 'react';
import "./BubbleBoxes.css";

class BubbleBoxes extends Component {
  
  render() {
    const { dataBoxes, color } = this.props;
    let boxes = dataBoxes.map((box, i) => {
      return (
      	<button className="btn btn-4 btn-4c" type="button" onClick={() => this.props.callback2FromParent(box)} key={box.topic}>
          {box.topic}
        </button>
      );
    });

    return (
      	<div>{boxes}</div>
    );
  }
}

BubbleBoxes.defaultProps = {
  dataBoxes: [],
  color: "#2196F3"
};

export default BubbleBoxes;