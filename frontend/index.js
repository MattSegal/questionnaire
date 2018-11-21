import ReactDOM from 'react-dom'
import React, { Component } from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import { Provider } from 'react-redux'

import { store } from 'state'
import BuilderForm from 'components/builder'
import FormGraph from 'components/form-graph'
import Header from 'components/header'
import Questionnaire from 'components/questionnaire'

import 'styles/main.global.scss'

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <div className="container">
            <div className="row">
              <div className="col">
                <Header />
                <Switch>
                  <Route path="/test">
                    <Questionnaire />
                  </Route>
                  <Route path="/graph">
                    <FormGraph />
                  </Route>
                  <Route path="/">
                    <BuilderForm />
                  </Route>
                </Switch>
              </div>
            </div>
          </div>
       </BrowserRouter>
      </Provider>
    )
  }
}

ReactDOM.render(<App/>, document.getElementById('app'))
