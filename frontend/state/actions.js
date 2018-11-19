module.exports = {
  question: {
    add: (name) => ({type: 'ADD_QUESTION', name}),
    remove: (name) => (({type: 'REMOVE_QUESTION', name}))
  }
}
