TEST_SCRIPT = {
    'start': 'NAME',
    'data_fields': {
        'NAME',
        'EMAIL',
        'LIKES_RUNNING',
        'LAST_RAN',
        'RUNS_PER_WEEK',
        'FAVOURITE_SHOE',
        'RUNNING_SURFACES',
        'LIKES_GRASS',
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
                {'then': 'LIKES_GRASS', 'when': {'variable': 'RUNNING_SURFACES', 'condition': 'contains', 'value': 'Grass'}},
            ],
            'then': 'THANKS',
        },
        'LIKES_GRASS': {
            'prompt': 'Do you like running on grass?',
            'type': 'boolean',
        },
        'THANKS': {
            'prompt': 'Cool, thanks!',
            'type': 'info',
        },
    }
}
