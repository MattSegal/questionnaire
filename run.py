"""
data types
    text
    number
    date
    email
    phone
    name
    address
    file
    image
    single choice
    multiple choice
    boolean

spec
    field
    question
    options
    type
    text
    follows
    when
        is
        is not
        contains
        not contains
        is greater than
        is less than


- behavioural tests
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
"""
import yaml

import spec_validator


def main():
    with open('landlord.yml', 'r') as f:
        spec = yaml.load(f)

    errors = spec_validator.validate(spec)
    if errors:
        print('\nFound errors parsing this questionnaire:')
        for error in errors:
            print('\t', error)

        print('')
        return




if __name__ == '__main__':
    main()