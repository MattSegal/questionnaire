const question = {
  ADD_QUESTION: (state, action) => ({
    ...state,
    script: {
      ...state.script,
      start: action.question.start ? action.question.start : state.script.start,
      dataFields: [...new Set([...state.script.dataFields, action.question.name])],
      steps: {
        ...state.script.steps,
        [action.question.name]: action.question,
      }
    }
  }),
  REMOVE_QUESTION: (state, action) => ({
    ...state,
    script: {
      ...state.script,
      steps: Object.keys(state.script.steps)
      .filter(key => key !== action.name)
      .reduce((newScript, key) => ({ ...newScript, [key]: state.script[key] }), {}),
    }
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
