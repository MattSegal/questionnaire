import React, { Component } from 'react'
import { connect } from 'react-redux'
import { actions } from 'state'
import ScriptValidator from 'validator'
import {
  FIELD_KEYS,
  FIELD_TYPES,
  CONDITIONS,
  MANDATORY_FIELDS,
} from 'consts'

const FIELD_TYPES_DISPLAY = {
  'text': 'Text',
  'email': 'Email',
  'multiple choice': 'Multiple Choice',
  'single choice': 'Single Choice',
  'boolean': 'Yes / No',
  'date': 'Date',
  'info': 'Information',
  'number': 'Number',
}


export default class AddQuestionForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      errors: {},
      // Question fields
      name: '',
      prompt: '',
      type: '',
    }
  }

  onNameInput = e =>
    this.setState({ name: e.target.value })

  onPromptInput = e =>
    this.setState({ prompt: e.target.value })

  onTypeInput = e =>
    this.setState({ type: e.target.value })

  onSubmit = e => {
    const question = this.getQuestion()
    const validator = new ScriptValidator(this.props.script)
    const isValid = validator.canAddQuestion(question)
    if (isValid) {
      this.props.addQuestion(question)
    }
    this.setState({ errors: validator.errors})
  }

  getQuestion = () =>
    FIELD_KEYS
      .filter(k => this.state[k])
      .map(k => [k, this.state[k]])
      .reduce((obj, [k, v]) => ({...obj, [k]: v}), {})

  render() {
    const { name, prompt, type, validator, errors } = this.state
    const { addQuestion } = this.props
    return (
      <div>
        <div className="input-group mb-3">

          <div className="input-group-prepend">
            <span className="input-group-text">Name</span>
          </div>
          <input
            type="text"
            className="form-control"
            placeholder="eg. 'HAS_CONTACTED_LANDLORD'"
            value={name}
            onChange={this.onNameInput}
          />
        </div>

        <div className="input-group mb-3">
          <div className="input-group-prepend">
            <span className="input-group-text">Type</span>
          </div>
          <select className="form-control" onChange={this.onTypeInput} selected={type}>
            <option value="">Select a data type</option>
            {FIELD_TYPES.map(fieldType => (
              <option key={fieldType} value={fieldType}>{FIELD_TYPES_DISPLAY[fieldType]}</option>
            ))}
          </select>
        </div>

        <div className="input-group mb-3">
          <div className="input-group-prepend">
            <span className="input-group-text">Prompt</span>
          </div>
          <input
            type="text"
            className="form-control"
            placeholder="Question prompt - eg. 'Have you contacted your landlord?'"
            value={prompt}
            onChange={this.onPromptInput}
          />
        </div>

        <button className="btn btn-primary mb-2" onClick={this.onSubmit}
        >
          Add Question
        </button>
       {Object.entries(errors)
          .filter(([questionName, errors]) => errors.length > 0)
          .map(([questionName, errors]) => (
            <div key={questionName}>
              <h4 className="text-danger">
                Error for question {questionName}
              </h4>
              {errors.map(msg => (
                <div key={msg} className="alert alert-danger">
                  {msg}
                </div>
              ))}
            </div>
        ))}
      </div>
    )
  }
}



const mapStateToProps = state => ({
  script: state.script,
})
const mapDispatchToProps = dispatch => ({
    addQuestion: name => dispatch(actions.question.add(name)),
})
module.exports = connect(mapStateToProps, mapDispatchToProps)(AddQuestionForm)
