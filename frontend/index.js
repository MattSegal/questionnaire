import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import { Provider } from 'react-redux'

import { store } from 'state'
import BuilderForm from 'components/builder'
import Header from 'components/header'

import 'styles/main.global.scss'

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <div className="container">
          <div className="row">
            <div className="col">
              <Header />
              <BuilderForm />
            </div>
          </div>
        </div>
      </Provider>
    )
  }
}

ReactDOM.render(<App/>, document.getElementById('app'))
