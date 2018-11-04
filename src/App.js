import React, { Component } from "react";
import "./App.css";

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
      isPaneOpen: false
    };
  }

  componentDidMount() {
    Modal.setAppElement(this.el);
  }

  // createFakeTopicData() {
  //   const d = ["Linear Regression", "Linear Growth", "Linear Logistics", "Quadratic Regression", "ReLu"];
  //   const data = [];
  //   for (let x = 0; x <= d.length; x++) {
  //     data.push({ d[x], x, x });
  //   }
  //   return data;
  // }

  createFakeArrowData() {
    const d = ["Linear Regression", "Linear Growth", "Linear Logistics", "Quadratic Regression", "ReLu"];
    const data = [];
    for (let x1 = 0; x1 <= d.length*100; x1+= 100) {
      let x2 = x1+100;
      let y1 = x1+100;
      let y2 = x1-100;
      data.push({ x1, x2, y1, y2 });
    }
    return data;
  }

  render() {
    return (
      <div className="App">
        <div ref={ref => (this.el = ref)}>
          <button onClick={() => this.setState({ isPaneOpen: true })}>
            Click me to open right pane!
          </button>
          <BubbleChart data={this.createFakeArrowData()} />
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
