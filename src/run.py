import yaml

from .spec import parser, validator
from .script import executor

def main():
    with open('specs/landlord.yml', 'r') as f:
        spec = yaml.load(f)

    errors = validator.validate(spec)
    if errors:
        print('\nFound errors parsing this questionnaire:')
        for error in errors:
            print('\t', error)

        print('')
        return

    script = parser.parse(spec)
    import json
    print(json.dumps(script))
    # data = executor.execute(script)

if __name__ == '__main__':
    main()
