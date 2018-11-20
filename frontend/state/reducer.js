const question = {
  ADD_QUESTION: (state, action) => ({
    ...state,
    script: {
      ...state.script,
      [action.question.name]: action.question,
    }
  }),
  REMOVE_QUESTION: (state, action) => ({
    ...state,
    script: Object.keys(state.script)
      .filter(key => key !== action.name)
      .reduce((obj, key) => ({ ...obj, [key]: state.script[key] }), {}),
  }),
}

const script = {
  UPLOAD_SCRIPT: (state, action) => ({
    ...state,
    script: action.script,
  })
}

const reducers = {
  ...question,
  ...script,
}


module.exports =  (state, action) => {
  const func = reducers[action.type]
  if (!func) return {...state}
  return func(state, action)
}
