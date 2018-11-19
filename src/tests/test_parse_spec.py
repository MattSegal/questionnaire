"""
Tests to ensure that the spec is parsed into a script correctly.
"""
from ..spec import parser


def test_parser__gets_start_field():
    """
    Ensure the parser pulls the start field out of the spec
    """
    spec = {
        'A': {'prompt': 'This is A', 'type': 'info', 'then': 'C'},
        'B': {'prompt': 'This is B', 'type': 'info', 'then': 'A', 'start': True},
        'C': {'prompt': 'This is C', 'type': 'info'},
    }
    script = parser.parse(spec)
    assert script['start'] == 'B'


def test_parser__builds_data_fields():
    """
    Ensure the parser builds a data store for the form
    """
    spec = {
        'A': {'prompt': 'This is A', 'type': 'text'},
        'B': {'prompt': 'This is B', 'type': 'boolean', 'start': True},
        'C': {'prompt': 'This is C', 'type': 'number'},
    }
    script = parser.parse(spec)
    assert script['data_fields'] == {'A', 'B', 'C'}


def test_parser__then_with_single_option():
    """
    Ensure that a single option for the "then" field get parsed correctly
    """
    spec = {
        'QUESTION': {
            'prompt': 'A question?',
            'start': True,
            'type': 'boolean',
            'then': 'END',
        },
        'END': {'prompt': 'This is the end', 'type': 'info'},
    }
    script = parser.parse(spec)
    assert script['steps']['QUESTION']['then'] == 'END'


def test_parser__then_with_many_options():
    """
    Ensure that many options for the "then" field get parsed correctly
    """
    spec = {
        'QUESTION': {
            'prompt': 'A question?',
            'start': True,
            'type': 'boolean',
            'then': [
                {'then': 'END_A', 'when': 'QUESTION is True'},
                {'then': 'END_B', 'when': 'QUESTION is False'}],
        },
        'END_A': {'prompt': 'This is end A', 'type': 'info'},
        'END_B': {'prompt': 'This is end B', 'type': 'info'},
    }
    script = parser.parse(spec)
    assert script['steps']['QUESTION']['then'] == [
        {
            'then': 'END_A',
            'when': {
                'variable': 'QUESTION',
                'condition': 'is',
                'value': True
            }
        },
        {
            'then': 'END_B',
            'when': {
                'variable': 'QUESTION',
                'condition': 'is',
                'value': False
            }
        },
    ]


def test_parser__smoke_test():
    """
    Broad test of most parser features to try and catch any unspecified issues.
    This test tries to cover most features of the spec.

    This also serves as a general description of what the parser output should look like.
    """
    spec = {
        'NAME': {
            'prompt': 'What\'s your name?',
            'start': True,
            'type': 'text',
            'then': 'EMAIL'
        },
        'EMAIL': {
            'prompt': 'What\'s your email?',
            'type': 'email',
            'then': 'LIKES_RUNNING'
        },
        'LIKES_RUNNING': {
            'prompt': 'Do you like running?',
            'type': 'boolean',
            'then': [
                {'then': 'NOT_FOR_YOU', 'when': 'LIKES_RUNNING is False'},
                {'then': 'LAST_RAN'},
            ]
        },
        'NOT_FOR_YOU': {
            'prompt': 'Ok, I guess this survey is not for you. Bye!',
            'type': 'info',
        },
        'LAST_RAN': {
            'prompt': 'When did you last go running?',
            'type': 'date',
            'then': 'RUNS_PER_WEEK'
        },
        'RUNS_PER_WEEK': {
            'prompt': 'How many times did you go running last week?',
            'type': 'number',
            'then': 'FAVOURITE_SHOE'
        },
        'FAVOURITE_SHOE': {
            'prompt': 'What\'s your favourite running shoe?',
            'type': 'single choice',
            'options': ['Nike', 'Adidas', 'Puma'],
            'details': [{'then': 'NIKE_SUCKS', 'when': 'FAVOURITE_SHOE is Nike'}],
            'then': 'RUNNING_SURFACES',
        },
        'NIKE_SUCKS': {
            'prompt': 'Just FYI, Nike sucks!',
            'type': 'info',
        },
        'RUNNING_SURFACES': {
            'prompt': 'What kind of surfaces do you like to run on?',
            'type': 'multiple choice',
            'options': ['Grass', 'Asphalt', 'Water'],
            'details': [
                {'then': 'NIKE_SUCKS', 'when': 'RUNNING_SURFACES contains Water'},
                {'then': 'NIKE_SUCKS', 'when': 'RUNNING_SURFACES contains Grass'},
            ],
            'then': 'THANKS',
        },
        'THANKS': {
            'prompt': 'Cool, thanks!',
            'type': 'info',
        },
    }
    script = parser.parse(spec)
    expected_script = {
        'start': 'NAME',
        'data_fields': {
            'NAME',
            'EMAIL',
            'LIKES_RUNNING',
            'LAST_RAN',
            'RUNS_PER_WEEK',
            'FAVOURITE_SHOE',
            'RUNNING_SURFACES',
        },
        'steps': {
            'NAME': {
                'prompt': 'What\'s your name?',
                'start': True,
                'type': 'text',
                'then': 'EMAIL'
            },
            'EMAIL': {
                'prompt': 'What\'s your email?',
                'type': 'email',
                'then': 'LIKES_RUNNING'
            },
            'LIKES_RUNNING': {
                'prompt': 'Do you like running?',
                'type': 'boolean',
                'then': [
                    {'then': 'NOT_FOR_YOU', 'when': {'variable': 'LIKES_RUNNING', 'condition': 'is', 'value': False}},
                    {'then': 'LAST_RAN'},
                ]
            },
            'NOT_FOR_YOU': {
                'prompt': 'Ok, I guess this survey is not for you. Bye!',
                'type': 'info',
            },
            'LAST_RAN': {
                'prompt': 'When did you last go running?',
                'type': 'date',
                'then': 'RUNS_PER_WEEK'
            },
            'RUNS_PER_WEEK': {
                'prompt': 'How many times did you go running last week?',
                'type': 'number',
                'then': 'FAVOURITE_SHOE'
            },
            'FAVOURITE_SHOE': {
                'prompt': 'What\'s your favourite running shoe?',
                'type': 'single choice',
                'options': ['Nike', 'Adidas', 'Puma'],
                'details': [{'then': 'NIKE_SUCKS', 'when': {'variable': 'FAVOURITE_SHOE', 'condition': 'is', 'value': 'Nike'}}],
                'then': 'RUNNING_SURFACES',
            },
            'NIKE_SUCKS': {
                'prompt': 'Just FYI, Nike sucks!',
                'type': 'info',
            },
            'RUNNING_SURFACES': {
                'prompt': 'What kind of surfaces do you like to run on?',
                'type': 'multiple choice',
                'options': ['Grass', 'Asphalt', 'Water'],
                'details': [
                    {'then': 'NIKE_SUCKS', 'when': {'variable': 'RUNNING_SURFACES', 'condition': 'contains', 'value': 'Water'}},
                    {'then': 'NIKE_SUCKS', 'when': {'variable': 'RUNNING_SURFACES', 'condition': 'contains', 'value': 'Grass'}},
                ],
                'then': 'THANKS',
            },
            'THANKS': {
                'prompt': 'Cool, thanks!',
                'type': 'info',
            },
        }
    }
    assert expected_script['start'] == script['start']
    assert expected_script['data_fields'] == script['data_fields']
    for step_name, step in expected_script['steps'].items():
        assert expected_script['steps'][step_name] == script['steps'].get(step_name), 'Error comparing step {}'.format(step_name)
