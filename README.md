# Questionnaire

This a proof of concept project.

I would like to see if we can create a flexible specification format for questionnaires. An example questionnaire:

```

Hi, welcome to our complaint form! what's your name?
> Matt

Ok Matt! What would you like to complain about?
    - A) The food was cold
    - B) My waiter was rude
    - C) The wait-time was too long
> C

You had to wait a long time? That sucks! How many minutes did you wait for your food?
> 20

That's longer than our guaranteed wait time, would you like a free food voucher? (y/n)

... etc

```

A business user will specifiy the form by creating a YAML file (see `forms/`).
The form spec will be parsed into an JSON script (see `src/spec`)
The JSON script can then be executed by a program that takes the script as an input, for example:

- a web application
- a phone app
- a CLI app (see `src/script`)

These apps will return a data object which can be stored sever-side:

```json
{
    "COST_OF_DAMAGES": null,
    "COUCH_FIRE_TIME": null,
    "COUCH_ISSUES": ["It is on fire"],
    "COUCH_MISSING": null,
    "COUCH_SMELL_RATING": null,
    "EMAIL": "mattdsegal@gmail.com",
    "HAS_CONTACTED_LANDLORD": true,
    "NAME": "Matt"
}
```

A user can also create behavioural tests for their spec (see `forms/`) which can be run on the spec programmatically.

**Possible Data Types**

- text
- number
- date
- email
- phone
- name
- address
- file
- image
- single choice
- multiple choice
- boolean

## Development

```bash
# Setup virtual env, requires virtualenv + python3
make setup

# Run unit tests
make test

# Run questionnaire
make run
```

## TODO

- get details working
- add unit tests
- each question needs a hint
- each answer option needs hint
- nail down YAML format
- run behavioural tests
- parser to validate input
    - correct values
    - correct operators
    - references to a valid name
- JSON output for execution
- command line tool that executes questionnaire
- data types with custom parsers
- javascript tool that executes questionaire
- React framework that displays questionaire
- customisable component for each data type
- option to save (email a magic link)
- ability to go back and change answer (will invalidate other questions)
- template answer into future questions as variables
- allow questionnaire to double check critical answers
