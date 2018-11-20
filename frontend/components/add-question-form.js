import React, { Component } from 'react'
import { connect } from 'react-redux'
import { actions } from 'state'
import ScriptValidator from 'validator'
import InputField from 'components/generic/input-field'
import CheckboxField from 'components/generic/checkbox-field'
import DropdownField from 'components/generic/dropdown-field'
import Button from 'components/generic/button'
import ErrorList from 'components/generic/error-list'
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

const INITIAL_STATE = {
  errors: [],
  // Question fields
  name: '',
  prompt: '',
  type: '',
  then: '',
  start: false,
}

export default class AddQuestionForm extends Component {
  constructor(props) {
    super(props);
    this.state = {...INITIAL_STATE}
  }

  onInput = fieldName => e =>
    this.setState({ [fieldName]: e.target.value })

  onSubmit = e => {
    const question = this.getQuestion()
    const validator = new ScriptValidator(this.props.script)
    const isValid = validator.canAddQuestion(question)
    if (isValid) {
      this.props.addQuestion(question)
      this.setState({...INITIAL_STATE})
    } else {
      this.setState({ errors: validator.errors })
    }
  }

  getQuestion = () =>
    FIELD_KEYS
      .filter(k => this.state[k])
      .map(k => [k, this.state[k]])
      .reduce((obj, [k, v]) => ({...obj, [k]: v}), {})

  render() {
    const { name, start, prompt, type, then, validator, errors } = this.state
    const { addQuestion, script } = this.props
    return (
      <div>
        <InputField
          label="Name"
          type="text"
          placeholder="A description of the question eg. 'Has contacted landlord'"
          value={name}
          onChange={this.onInput('name')}
        />
        <InputField
          label="Prompt"
          type="text"
          placeholder="Question prompt - eg. 'Have you contacted your landlord?'"
          value={prompt}
          onChange={this.onInput('prompt')}
        />
        <DropdownField
          label="Type"
          placeholder="Select question data type"
          value={type}
          onChange={this.onInput('type')}
          options={FIELD_TYPES.map(fieldType => [fieldType, FIELD_TYPES_DISPLAY[fieldType]])}
        />
        <DropdownField
          label="Then"
          placeholder="Select the next question"
          value={then}
          onChange={this.onInput('then')}
          disabled={Object.keys(script).length < 1}
          options={Object.keys(script).map(k => [k, k])}
        />
        <CheckboxField
          label="Starting question"
          value={start}
          disabled={Object.values(script).some(q => q.start)}
          onChange={this.onInput('start')}
        />
        <ErrorList errors={errors} />
        <Button onClick={this.onSubmit} disabled={!name}>
          Add Question
        </Button>
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
