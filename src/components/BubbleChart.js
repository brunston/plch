import React, { Component } from "react";
import "./BubbleChart.css";

class BubbleChart extends Component {
  // GET MAX & MIN X
  getMinX() {
    const { data } = this.props;
    return data.reduce((min, p) => (p.x < min ? p.x : min), data[0].x);
  }
  getMaxX() {
    const { data } = this.props;
    return data.reduce((max, p) => (p.x > max ? p.x : max), data[0].x);
  }
  // GET MAX & MIN Y
  getMinY() {
    const { data } = this.props;
    return data.reduce((min, p) => (p.y < min ? p.y : min), data[0].y);
  }
  getMaxY() {
    const { data } = this.props;
    return data.reduce((max, p) => (p.y > max ? p.y : max), data[0].y);
  }

  getSvgX(x) {
    const { svgWidth } = this.props;
    return (x / this.getMaxX()) * svgWidth;
  }
  getSvgY(y) {
    const { svgHeight } = this.props;
    return svgHeight - (y / this.getMaxY()) * svgHeight;
  }

  render() {
    const { data, svgHeight, svgWidth } = this.props;
    let pathD = data.map((line, i) => {
    	let x_1 = this.getMaxX();
      return (
        <line className='bubbleline' key={line.x1.toString() + " " + line.y1.toString() + " " + line.x2.toString() + " " + line.y2.toString() + " " }
         x1= {line.x1} //this.getSvgX(line.x1)
         y1= {line.y1} //this.getSvgY(line.y1)
         x2= {line.x2} //this.getSvgX(line.x2)
         y2= {line.y2} //this.getSvgY(line.y2)
         stroke="black" stroke-width="10" stroke-linecap="square"
        /> 
      );
    });

    return (
      <div className="window">
        <svg viewBox={`0 0 ${svgWidth} ${svgHeight}`}>{pathD}</svg>
      </div>
    );
  }
}

BubbleChart.defaultProps = {
  data: [],
  color: "#2196F3",
  svgHeight: 700,
  svgWidth: 700
};
export default BubbleChart;
