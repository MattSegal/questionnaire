import {
  FIELD_KEYS,
  FIELD_TYPES,
  CONDITIONS,
  MANDATORY_FIELDS,
} from 'consts'

// Used to validate new questions, which are added to the script.
export default class ScriptValidator {
  constructor(script) {
    this.start = script.start
    this.dataFields = script.data_fields
    this.steps = script.steps
    this.errors = {}
  }

  // Returns true if the question being added is valid
  canAddQuestion = q => {
    this.errors = this.getQuestionNames(q)
      .reduce((obj, key) => ({...obj, [key]: []}), {})

    // Do initial validation
    this.validateMandatoryFields(q)
    this.validateFieldWhitelist(q)
    // Bail if initial validation fails
    if (this.hasErrors()) return false
    // Validate each field
    const fieldValidators = {
      'name': this.validateName,
      'start': this.validateStart,
      'type': this.validateType,
      'options': this.validateOptions,
      'help': this.validateHelp,
      'details': this.validateDetails,
      'then': this.validateThen,
      'prompt': this.validatePrompt,
    }
    for (let fieldName of Object.keys(q)) {
      fieldValidators[fieldName](q)
    }
    return !this.hasErrors()
  }

  // All mandatory fields should be present
  validateMandatoryFields = q => {
    for (let fieldName of MANDATORY_FIELDS) {
      if (!q[fieldName]) {
        this.addError(q, `Field "${fieldName}" is required.`)
      }
    }
  }

  // All fields should be from the whitelust
  validateFieldWhitelist  = q => {
    for (let fieldName of Object.keys(q)) {
      if (!FIELD_KEYS.includes(fieldName)) {
        console.error(fieldName, FIELD_KEYS)
        this.addError(q, `Field "${fieldName}" is not allowed.`)
      }
    }
  }

  // Validate the 'start' field.
  validateStart = q => {
    if (this.start && q.start) {
      this.addError(q, 'Cannot have two start questions.')
    } else if (typeof(q.start !== "boolean")) {
      this.addError(q, 'Start field must be "true" or "false"')
    }
  }

  // Validate the 'type' field.
  validateType = q => {
    if (!FIELD_TYPES.includes(q.type)) {
      this.addError(q, 'Invalid value for "type')
    }
    const typeValidators = {
      'text': q => {},
      'email': q => {},
      'multiple choice': this.validateMultipleChoice,
      'single choice': this.validateSingleChoice,
      'boolean': q => {},
      'date': q => {},
      'info': q => {},
      'number': q => {},
    }
    typeValidators[q.type](q)
  }

  // Validate the 'options' field.
  validateOptions = q => {
    if (typeof(q.options !== "object")) {
      this.addError(q, 'Options field must be a list')
    }
    if (!q.options.every(this.validateOption)) {
      this.addError(q, 'Each option must have a hint and text field')
    }
  }

  validateOption = option => (
    typeof(option) === "object" &&
    (!option.hint || typeof(option.hint) === "string") &&
    option.text && typeof(option.text) === "string"
  )

  // Validate the 'help' field.
  validateHelp = q => {
    if (q.help && typeof(q.help !== "string")) {
      this.addError(q, 'The "help" field must only contain text.')
    }
  }

  // Validate the 'details' field.
  validateDetails = q => {
    if (typeof(q.details !== "object")) {
      this.addError(q, 'Details field must be a list')
    } else {
      for (let detail of q.details) {
        this.validateConditionalThen(q, detail, 'detail')
      }
    }
  }

  // Validate the 'then' field.
  validateThen = q => {
    if (typeof(q.then === "string")) {
      if (!this.getQuestionNames(q).includes(q.then)) {
        this.addError(q, 'The "then" field must reference another question')
      }
    } else if (typeof(q.then === "object")) {
      for (let then of q.then) {
        this.validateConditionalThen(q, then, 'then')
      }
    } else {
      this.addError(q, 'The "then" field must be a string or list')
    }
  }

  validateConditionalThen = (q, conditionalThen, fieldName) => {
    const then = conditionalThen.then
    const when = conditionalThen.when
    if (!then || !this.getQuestionNames(q).includes(then)) {
      this.addError(q, `The ${fieldName} field must have a "then" field which references another question`)
    }
    if (!when) return
    if (!when.variable || !when.condition || !when.value) {
      this.addError(q, `The ${fieldName} field must have a "when" field which has a variable, condition and value`)
      return
    }
    if (!this.getQuestionNames(q).includes(when.variable)) {
      this.addError(q, `The ${fieldName} field\'s "when" variables must reference another question`)
    }
    if (!(when.condition in CONDITIONS)) {
      this.addError(q, `The ${fieldName} field\'s "when" conditions must be a valid condition.`)
    }
  }

  // Validate the 'prompt' field.
  validatePrompt = q => {
    if (typeof(q.prompt) !== "string") {
      this.addError(q, 'The "prompt" field must only contain text.')
    }
  }

  // Validate the 'name' field.
  validateName = q => {
    if (typeof(q.name) !== "string") {
      this.addError(q, 'The "name" field must only contain text.')
    }
  }

  // Validate a 'multiple choice' type question.
  validateMultipleChoice = q => {
    if (!q.options) {
      this.addError(q, 'Multiple choice questions must have options')
    }
  }

  // Validate a 'single choice' type question.
  validateSingleChoice = q => {
    if (!q.options) {
      this.addError(q, 'Single choice questions must have options')
    }
  }

  // Get a list of all possible question names
  getQuestionNames = q => [
    ...Object.keys(this.steps),
    q.name
  ]

  // Add error to the error list
  addError = (q, msg) =>
    this.errors[q.name].push(msg)

  // Get a count for how many errors we have
  getErrorCount = () =>
    Object.values(this.errors)
      .map(arr => arr.length)
      .reduce((a, b) => a + b, 0)

  // Returns true if the validator has errors
  hasErrors = () =>
    this.getErrorCount() > 0
}
