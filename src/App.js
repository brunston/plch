import React, { Component } from "react";
import "./App.css";
import "./components/BubbleBoxes.css";

import { render } from "react-dom";
import Modal from "react-modal";
import SlidingPane from "react-sliding-pane";
import BubbleChart from "./components/BubbleChart";
import HTMLViewer from "./components/HTMLViewer";
import "react-sliding-pane/dist/react-sliding-pane.css";

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      isPaneOpen: false,
      currTopic: "Linear Logistics"
    };
  }

  componentDidMount() {
    Modal.setAppElement(this.el);
  }

  createFakeTopicData() {
    const d = ["Linear Regression", "Linear Growth", "Quadratic Regression", "ReLu"];
    const o = [-1, -1, 1, 1];
    const data = [];
    for (let x = 0; x <= d.length; x++) {
      let topic = d[x];
      let order = o[x];
      data.push({ topic, order });
    }
    return data;
  }

  // createFakeArrowData() {
  //   const d = ["Linear Regression", "Linear Growth", "Linear Logistics", "Quadratic Regression", "ReLu"];
  //   const x1s = [150, 150, 400, 400];
  //   const y1s = [200,  50, 200,  50];
  //   const x2s = [270, 270, 270, 270];
  //   const y2s = [130, 130, 130, 130];
  //   const data = [];
  //   for (let i = 0; i < x1s.length; i++) {
  //     let x1 = x1s[i];
  //     let y1 = y1s[i];
  //     let x2 = x2s[i];
  //     let y2 = y2s[i];
  //     data.push({ x1, x2, y1, y2 });
  //   }
  //   return data;
  // }

  render() {
    let currDataBoxes = this.createFakeTopicData().filter((boxes, i) => {
      return boxes.order == 0;
    });
    return (
      <div className="App">
        <div ref={ref => (this.el = ref)}>
          <button className="btn btn-4 btn-4c" key={currDataBoxes.topic} onClick={() => this.setState({ isPaneOpen: true })}>
            {this.state.currTopic}
          </button>
          <BubbleChart dataBoxes={this.createFakeTopicData()}/>
          <SlidingPane
              className='some-custom-class'
              overlayClassName='some-custom-overlay-class'
              isOpen={ this.state.isPaneOpen }
              title='PDF Viewer'
              onRequestClose={ () => {
                  // triggered on "<" on left top click or on outside click
                  this.setState({ isPaneOpen: false });
              } }>
              <br />
              <HTMLViewer />
          </SlidingPane>
        </div>
      </div>
    );
  }
}
export default App;
