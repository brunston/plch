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
      isPaneOpen: false,
      currTopic: "Start",
      currOrder: 0,
      data: [],
      docIds: []
    };
    // this.state.data = this.createFakeTopicData();
    this.state.data = [];
  }

  myCallback(dataFromChild) {
    this.setState({ currTopic: dataFromChild.topic });
    this.setState({ currOrder: dataFromChild.order });
  }


  createFakeTopicData() {
    const d = ["Linear Regression", "Linear Growth", "Quadratic Regression", "ReLu", "Machine Learning"];
    const o = [-1, -1, 1, 2, 3];
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

  componentDidMount() {
    Modal.setAppElement(this.el);
    fetch('http://b15da023.ngrok.io/api/v0.1/corpus', {mode: 'cors'})
    .then(results => {
      console.log(results);
      return results.json();
    }).then(data => {
        this.state.docIds = data;
        let doc = this.state.docIds;
        for (var i = 0; i < 10; i++)
        {
            // Do something
            let id = doc[i];
            fetch('http://b15da023.ngrok.io/api/v0.1/corpus/text/' + id + '/heading', {mode: 'cors'})
            .then(results2 => {
              return results2.json();
            }).then(data2 => {
                console.log(data2);
                let topic = data2[0];
                let order = id;
                this.state.data.push({ topic, order });
            })        
        }        
    }) 

    
  }

  render() {
    return (
      <div className="App">
        <div ref={ref => (this.el = ref)}>
          <button className="btn btn-4 btn-4c" onClick={() => this.setState({ isPaneOpen: true })}>
            {this.state.currTopic}
          </button>
          <BubbleChart dataBoxes={this.state.data} callbackFromParent={this.myCallback.bind(this)}/>
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
              <img src={require('./files/pdff.png')} style={{width:"1000px"}}/>
          </SlidingPane>
        </div>
      </div>
    );
  }
}
export default App;
