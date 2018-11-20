module.exports = {
  question: {
    add: (question) => ({type: 'ADD_QUESTION', question}),
    remove: (name) => (({type: 'REMOVE_QUESTION', name}))
  },
  script: {
    upload: script => ({type: 'UPLOAD_SCRIPT', script}),
  }
}
