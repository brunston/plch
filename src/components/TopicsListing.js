import React, { Component } from 'react';

export default class TopicsListing extends Component {
  render() {
    return (
      <div className="topicslisting">
        { this.props.children }
      </div>
    )
  }
}
