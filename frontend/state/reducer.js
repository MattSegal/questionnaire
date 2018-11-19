const question = {
  ADD_QUESTION: (state, action) => ({
    ...state,
    script: {
      ...state.script,
      [action.name]: {},
    }
  }),
  REMOVE_QUESTION: (state, action) => ({
    ...state,
    script: Object.keys(state.script)
      .filter(key => key !== action.name)
      .reduce((newScript, key) => ({ ...newScript, [key]: state.script[key] }), {}),
  }),
}


const reducers = {
  ...question,
}


module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
