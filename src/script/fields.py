"""
display questoions for each field type
validate data input for each field type
"""

def get_user_input(step, data):
    # Replace prompt with templated values
    prompt = step['prompt'].format(**data)
    data_type = step['type']
    try:
        return DATA_COLLECTIORS[data_type](prompt, step, data)
    except Exception:
        print('Step:', step)
        print('Data:', data)
        raise


DATA_COLLECTIORS = {
    'text': lambda *args: TextCollector(*args).collect(),
    'email': lambda *args: EmailCollector(*args).collect(),
    'multiple choice': lambda *args: MultipleChoiceCollector(*args).collect(),
    'single choice': lambda *args: SingleChoiceCollector(*args).collect(),
    'boolean': lambda *args: BooleanCollector(*args).collect(),
    'date': lambda *args: DateCollector(*args).collect(),
    'info': lambda *args: InfoCollector(*args).collect(),
    'number': lambda *args: NumberCollector(*args).collect(),
}


class DataCollector:
    def __init__(self, prompt, step, data):
        self.prompt = prompt
        self.step = step
        self.data = data

    def print_error(self):
        print('You must provide an answer to continue\n')

    def get_prompt(self):
        return self.prompt + '\n\n\t'

    def is_response_valid(self, response):
        return bool(response)

    def collect(self):
        response = None
        while not self.is_response_valid(response):
            response = input(self.get_prompt())
            print()
            if not self.is_response_valid(response):
                self.print_error()

        return response

class TextCollector(DataCollector):
    pass


class EmailCollector(DataCollector):
    def print_error(self):
        print('You must provide a valid email to continue\n')

    def is_response_valid(self, response):
        return response and '@' in response and '.' in response


class MultipleChoiceCollector(DataCollector):
    OPTIONS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, *args):
        super().__init__(*args)
        self.options = self.step['options']

    def print_error(self):
        print('You must provide at least one an answer to continue\n')

    def get_prompt(self):
        return (
            self.prompt + '\n' +
            'Your options are' + '\n\t' +
            '\n\t'.join([
                '- {}) {}'.format(self.OPTIONS[idx], self.options[idx]) for idx
                in range(len(self.options))
            ]) + '\n'
        )
    def is_response_valid(self, response):
        return response and all([
            r in self.OPTIONS[:len(self.options)]
            for r in response
        ])

    def collect(self):
        response = super().collect()
        response_idx = self.OPTIONS.index(response)
        return self.options[response_idx]


class SingleChoiceCollector(MultipleChoiceCollector):
    def print_error(self):
        print('You must provide exactly one an answer to continue\n')

    def is_response_valid(self, response):
        return response and len(response) == 1 and all([
            r in self.OPTIONS[:len(self.options)]
            for r in response
        ])


class BooleanCollector(SingleChoiceCollector):
    OPTIONS = ['y', 'n']

    def __init__(self, *args):
        super(MultipleChoiceCollector, self).__init__(*args)
        self.options = [True, False]

    def print_error(self):
        print('You must answer "yes" or "no" continue\n')


class DateCollector(DataCollector):
    pass


class InfoCollector(DataCollector):
    pass


class NumberCollector(DataCollector):
    pass

