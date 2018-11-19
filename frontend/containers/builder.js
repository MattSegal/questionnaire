import React, { Component } from 'react'
import { connect } from 'react-redux'
import { actions } from 'state'

export default class BuilderContainer extends Component {

  constructor(props) {
    super(props);
    this.state = {
      name: '',
    }
  }

  onNameInput = e =>
    this.setState({ name: e.target.value })

  render() {
    const { name } = this.state
    const { script, addQuestion, removeQuestion } = this.props
    return (
      <div>
        {Object.keys(script).map(k => (
          <div key={k}>
            <h2>{ k }</h2>
            <button onClick={() => removeQuestion(k)}>Remove</button>
          </div>
        ))}
        <input value={name} onChange={this.onNameInput} />
        <button onClick={() => addQuestion(name)}>Add Question</button>
      </div>
    )
  }
}



const mapStateToProps = state => ({
  script: state.script,
})
const mapDispatchToProps = dispatch => ({
    addQuestion: name => dispatch(actions.question.add(name)),
    removeQuestion: name => dispatch(actions.question.remove(name)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(BuilderContainer)
