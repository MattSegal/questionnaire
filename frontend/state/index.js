import { applyMiddleware, createStore } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger }  from 'redux-logger'

import reducer from './reducer'
import actions from './actions'
import initialState from './init'

const loggerMiddleware = createLogger()
const middleware = applyMiddleware(thunkMiddleware, loggerMiddleware)
const store = createStore(reducer, initialState, middleware)

module.exports = { store, actions }
