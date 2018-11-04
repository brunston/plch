import React, { Component } from 'react';

export default class BubbleBoxes extends Component {
  render() {
    return (
      <div className="bubbleboxes">
        { this.props.children }
      </div>
    )
  }
}
