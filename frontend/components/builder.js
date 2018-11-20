import React, { Component } from 'react'
import { connect } from 'react-redux'

import AddQuestionForm from 'components/add-question-form'
import Question from 'components/question'

export default class BuilderForm extends Component {

  render() {
    const { script } = this.props
    return (
      <div>
        <AddQuestionForm />
        <h2 className="mt-3">Questions</h2>
        {Object.keys(script)
          .map(k => (
            <Question key={k} question={script[k]} />
          )
        )}
      </div>
    )
  }
}


const mapStateToProps = state => ({
  script: state.script,
})
const mapDispatchToProps = dispatch => ({})
module.exports = connect(mapStateToProps, mapDispatchToProps)(BuilderForm)
