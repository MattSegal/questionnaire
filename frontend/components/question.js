import React, { Component } from 'react'
import { connect } from 'react-redux'
import { actions } from 'state'


export default class Question extends Component {

  render() {
    const { question, removeQuestion } = this.props
    return (
      <div>
        <h2>{ question.name }</h2>
        <button onClick={() => removeQuestion(question.name)}>Remove</button>
      </div>
    )
  }
}



const mapStateToProps = state => ({
  script: state.script,
})
const mapDispatchToProps = dispatch => ({
    removeQuestion: name => dispatch(actions.question.remove(name)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(Question)
