import React, { Component } from 'react'
import { connect } from 'react-redux'
import Dracula from 'graphdracula'

const Graph = Dracula.Graph;
const Renderer = Dracula.Renderer.Raphael;
const Layout = Dracula.Layout.Spring;



class FormGraph extends Component {

  componentDidMount() {
    this.drawGraph()
  }

  componentDidUpdate() {
    this.drawGraph()
  }

  drawGraph() {
    const { script } = this.props
    const graph = new Graph();
    for (let question of Object.values(script)) {
      if (question.then) {
        graph.addEdge(question.name, question.then, { directed: true });
      }
    }
    const layout = new Layout(graph)
    const renderer = new Renderer('#graph', graph, 800, 500);
    renderer.draw()
  }

  render() {
    return <div id="graph" />
  }
}


const mapStateToProps = state => ({
  script: state.script,
})
const mapDispatchToProps = dispatch => ({})
module.exports = connect(mapStateToProps, mapDispatchToProps)(FormGraph)
