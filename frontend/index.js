import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import { Provider } from 'react-redux'

import { store } from 'state'
import BuilderContainer from 'containers/builder'
import 'styles/main.scss'

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <div className="container">
          <div className="row">
            <div className="col">
              <h1>Questionnaire Form Builder</h1>
            </div>
          </div>
          <BuilderContainer />
        </div>
      </Provider>
    )
  }
}

ReactDOM.render(<App/>, document.getElementById('app'))
